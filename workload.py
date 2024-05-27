import argparse
import os
import cv2
import time

from SPARQLWrapper import SPARQLWrapper, JSON


def run(endpoint: str, save_folder: str, repeat: int = 1):
    """ Run workload based on semantified results on Fuseki
        
    Args:
        endpoint: SPARQL endpoint to run query
        save_folder: Where to save the annotated files with detected people
        repeat: Repeat how many times for generating the workload with current data
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    ## Query frames inserted into Fuseki
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX glc: <https://glaciation-project.eu/reference_model#>

        SELECT *
        WHERE {
        ?frame rdf:type glc:YOLOResult .
        ?frame glc:fileLocation ?loc .
        ?frame glc:hasDetection ?detection .
        ?detection glc:hasLabel ?label;
          		   glc:hasConfidence ?conf .
        ?detection glc:hasBBox ?bbox .
        ?bbox glc:hasX ?x;
              glc:hasY ?y;
              glc:hasWidth ?w;
              glc:hasHeight ?h .
        }
    """)

    try: 
        for i in range(repeat):
            res = sparql.queryAndConvert()
            for r in res['results']['bindings']:
                # Get UUID
                uuid = r['frame']['value'].split('#')[1]
                # Get label
                label = r['label']['value']
                #if label == 'person':
                # Get image location
                file_loc = os.path.join(r['loc']['value'], uuid)
                image = cv2.imread(file_loc)
                # Draw bounding box
                new_img = cv2.rectangle(
                    image, 
                    (int(r['x']['value']), int(r['y']['value'])),
                    (int(r['x']['value'])+int(r['w']['value']), int(r['y']['value'])+int(r['h']['value'])),
                    (0, 255, 0),
                    5
                )
                # Save into separate folder
                cv2.imwrite(
                    os.path.join(save_folder, uuid+'.png'), new_img
                ) 
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint', default='http://10.244.0.37:3030/ds/query')
    parser.add_argument('-d', '--destination', defualt='../people_detection_results')
    parser.add_argument('-r', '--repeat', default=1)
    args = parser.parse_args()

    start_time = time.perf_counter()

    ## Workload
    run(
        args.endpoint,
        args.destination,
        args.repeat
    )

    end_time = time.perf_counter()
    print(f'{end_time - start_time} seconds elapsed')

