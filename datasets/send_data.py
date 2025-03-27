import argparse
import os
import sys
import requests
import json
import time
import logging

from pyld import jsonld
from SPARQLWrapper import (
    SPARQLWrapper, 
    JSON, 
    POST
)


# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
cons_handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s -- %(message)s')
cons_handler.setFormatter(formatter)
logger.addHandler(cons_handler)

UC2_GRAPH_URI = 'https://glaciation-project.eu/uc/2'


def expand_json(jf: dict, robot_id: str):
    """Expand JSON to JSON-LD except image_base64

    Args:
        jf: Json file loaded
        robot_id: identifier of data from which robot
    
    Returns:
        expanded Json file
    """

    # Context list
    jf['@context'] = {
       "@vocab": "https://glaciation-project.eu/MetadataReferenceModel#",
       "odrl": "http://www.w3.org/ns/odrl/2/",
       "dpv": "https://w3id.org/dpv#",
       "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
       "saref": "https://saref.etsi.org/core/",
       "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
    }

    # Add back later 
    temp_image_base64 = jf['image_base64']
    jf.pop('image_base64')
    logger.debug(f'Json file:\n{jf}')

    jf['@type'] = 'saref:Device'
    jf['saref:hasIdentifier'] = robot_id

    ## Process detections
    if 'detections' in jf:
        # Make measurement list
        yolo_results = []
        for detection in jf['detections']:
            measurements = []
            for field in ['class', 'name', 'confidence', 'x1', 'x2', 'y1', 'y2']:
                measurements.append({
                    '@type': 'Measurement',
                    'saref:hasValue': detection[field] if field in ['class', 'name', 'confidence'] else detection['bounding_box'][field],
                    'saref:relatesToProperty': {'@id': jf['@context']['@vocab']+field, '@type': 'saref:Property'}
                })

            yolo_results.append(
                {
                    '@type': 'YOLO',
                    'rdf:subClassOf': {'@type':'MeasuringResource'},
                    'makesMeasurement': measurements
                }
            )

        # Make each YOLO results
        jf['hasSubResource'] = yolo_results
        # Pop processed
        jf.pop('detections')

    ## Process properties
    jf['saref:hasDeviceKind'] = {
        '@type': 'saref:Sensor',
    }

    props = []
    for prop in jf['metadata']:
        logger.debug(f'Appending property: {prop}')
        props.append({
            '@id': f'{jf["@context"]["@vocab"]}/{prop}' if ':' not in prop else jf['@context'][prop.split(':')[0]]+prop.split(':')[1],
            '@type': 'saref:Property',
            'saref:hasPropertyValue': {
                '@type': 'saref:PropertyValue',
                'saref:hasValue': jf['metadata'][prop]
            }
        })
        jf['saref:hasDeviceKind']['saref:hasProperty'] = props
    jf.pop('metadata')

    expanded = jsonld.expand(jf)[0]
    # Add graph info so that usecase triples always being inserted into this graph
    graph = {}
    graph['@graph'] = [expanded]
    #graph['@id'] = UC2_GRAPH_URI
    # Add image, will be separated in Apache NiFi pipeline later
    graph['image_base64'] = temp_image_base64

    return graph


def delete(jena_url: str):
    """ Query a list of named graphs in DKG
        Delete them 
    """
    # Query and get list of named graphs
    query_endpoint = jena_url + '/' + 'query'
    update_endpoint = jena_url + '/' + 'update'
    logger.info(f'SPARQL endpoint: {query_endpoint}\n{update_endpoint}')
    sparql = SPARQLWrapper(
        endpoint=query_endpoint,
        updateEndpoint=update_endpoint
    )
    sparql.setTimeout(60)
    # Query for named graphs
    query = """
    SELECT DISTINCT ?graph
    WHERE {
        GRAPH ?graph {
            ?s ?p ?o.
        }
    """
    query += f'FILTER(STRSTARTS(STR(?graph), "{UC2_GRAPH_URI}"))' + '}'
    logger.debug(f'Query: {query}')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
    except Exception as e:
        logger.error(f'Error executing SPARQL SELECT query to JENA: {e}')
        results = {'results': {'bindings':[]}}

    # Delete them
    if len(results['results']['bindings']) > 0:
        sparql.setMethod(POST)
        for result in results['results']['bindings']:
            try:
                graph_uri = result['graph']['value']
                drop_query = f'DROP GRAPH <{graph_uri}>'
                logger.debug(f'Deleting graph URI: {graph_uri}, query: {drop_query}')
                sparql.setQuery(drop_query)
                sparql.query()
                time.sleep(2)
            except Exception as e:
                logger.error(f'Error executing SPARQL DRAP Graph to JENA: {e}')


def main(
    nifi_url: str = "http://semantification.validation/contentListener",
    jena_url: str = 'http://jena-fuseki.validation/#/dataset/slice',
    data_dir: str = "~/DELL-UC/datasets",
    subdirectories: list = ["robot_0", "robot_1", "robot_2", "robot_5", "robot_7"],
    test_mode: bool = False,
    delete_first: bool = False
) -> None:
    """
    Args:
        nifi_url: Define the base URL for the Apache NiFi endpoint
        data_dir: Dataset directory
        sub_directories: List of subdirectories (e.g., robot_0, robot_1, etc.)
        test_mode: Run only once for testing
        delete_first: Delete previous named graphs from DKG before sending the data
    """
    if delete_first:
        delete(jena_url)
    # Base directory where the datasets are located
    base_dir = os.path.expanduser(data_dir)
    
    # Iterate through each subdirectory
    count = 0
    for subdir in subdirectories:
        subdir_path = os.path.join(base_dir, subdir)
        
        # Iterate through each JSON file in the subdirectory
        for filename in os.listdir(subdir_path):
            logger.info(f'\nProcessing file: {filename}')
            if filename.endswith(".json"):
                count += 1
                file_path = os.path.join(subdir_path, filename)
                
                # Read the JSON file
                with open(file_path, 'r') as file:
                    #json_data = file.read()
                    jf = json.load(file)
                
                expanded = expand_json(jf, subdir)
                #expanded.pop('image_base64')
                logger.debug(f'Json:\n{json.dumps(expanded, indent=2)}')
                json_data = json.dumps(expanded)
    
                # Send the JSON data to the Apache NiFi endpoint
                response = requests.post(
                    nifi_url, 
                    data=json_data, 
                    headers={"Content-Type": "application/json"}
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    logger.info(f"Successfully sent {filename} from {subdir} to Apache NiFi.")
                else:
                    logger.info(f"Failed to send {filename} from {subdir}. Status code: {response.status_code}")
                
            if test_mode:
                break
    
    logger.info(f"{count} files processed.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Sending data with optional arguments')

    parser.add_argument(
        '--nifi_url', 
        type=str, 
        default='http://semantification.integration/contentListener',
        help='ApacheNiFi content listener URL, default: http://semantification.integration/contentListener'
    )
    parser.add_argument(
        '--jena_url',
        type=str,
        default='http://jena-fuseki.integration/slice',
        help='ApacheJena prefix of endpoints, default: http://jena-fuseki.integration/slice'
    )
    parser.add_argument(
        '-t',
        '--test_mode',
        action='store_true',
        help='Bool, enable test mode to send only sample examples for testing'
    )
    parser.add_argument(
        '-d',
        '--delete',
        action='store_true',
        help='Delete all named graphs before sending data'
    )
    args = parser.parse_args()


    main(
        test_mode=args.test_mode,
        nifi_url=args.nifi_url,
        jena_url=args.jena_url,
        delete_first=args.delete
    )
