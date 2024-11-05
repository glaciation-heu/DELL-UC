import os
import requests
import json

from pyld import jsonld



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
    print(jf)

    jf['@type'] = 'saref:Device'
    jf['saref:hasIdentifier'] = robot_id

    ## Process detections
    if 'detections' in jf:
        # Make measurement list
        measurements = []
        for detection in jf['detections']:
            for field in ['class', 'name', 'x1', 'x2', 'y1', 'y2']:
                measurements.append({
                    '@type': 'Measurement',
                    'saref:hasValue': detection[field] if field in ['class', 'name'] else detection['bounding_box'][field],
                    'saref:relatesToProperty': {'@id': jf['@context']['@vocab']+field, '@type': 'saref:Property'}
                })

        jf['hasSubResource'] = {
            '@type': 'YOLO',
            'rdfs:subClassOf': {'@type':'MeasuringResource'},
            'makesMeasurement': measurements
        }

        # Pop processed
        jf.pop('detections')

    ## Process properties
    jf['saref:hasDeviceKind'] = {
        '@type': 'saref:Sensor',
    }

    props = []
    for prop in jf['metadata']:
        print(prop)
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
    expanded['image_base64'] = temp_image_base64

    return expanded


def main(
    nifi_url: str = "http://semantification.validation/contentListener",
    data_dir: str = "~/DELL-UC/datasets",
    subdirectories: list = ["robot_0", "robot_1", "robot_2", "robot_5", "robot_7"],
    test_mode: bool = False
) -> None:
    """
    Args:
        nifi_url: Define the base URL for the Apache NiFi endpoint
        data_dir: Dataset directory
        sub_directories: List of subdirectories (e.g., robot_0, robot_1, etc.)
        test_mode: Run only once for testing
    """
    # Base directory where the datasets are located
    base_dir = os.path.expanduser(data_dir)
    
    # Iterate through each subdirectory
    count = 0
    for subdir in subdirectories:
        subdir_path = os.path.join(base_dir, subdir)
        
        # Iterate through each JSON file in the subdirectory
        for filename in os.listdir(subdir_path):
            print(f'\nProcessing file: {filename}')
            if filename.endswith(".json"):
                count += 1
                file_path = os.path.join(subdir_path, filename)
                
                # Read the JSON file
                with open(file_path, 'r') as file:
                    #json_data = file.read()
                    jf = json.load(file)
                
                #jf.pop('image_base64')
                #print(f'{jf}')
                expanded = expand_json(jf, subdir)
                #expanded.pop('image_base64')
                print(json.dumps(expanded, indent=2))
                json_data = json.dumps(expanded)
    
                # Send the JSON data to the Apache NiFi endpoint
                response = requests.post(
                    nifi_url, 
                    data=json_data, 
                    headers={"Content-Type": "application/json"}
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    print(f"Successfully sent {filename} from {subdir} to Apache NiFi.")
                else:
                    print(f"Failed to send {filename} from {subdir}. Status code: {response.status_code}")
                
            if test_mode:
                break
    
    print(f"{count} files processed.")


if __name__ == '__main__':
    main(
        test_mode=False,
        nifi_url="http://semantification.integration/contentListener"
    )
