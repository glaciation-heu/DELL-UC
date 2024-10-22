import os
import requests
import json

from pyld import jsonld



def expand_json(jf: dict):
    """Expand JSON to JSON-LD except image_base64

    Args:
        jf: Json file loaded
    
    Returns:
        expanded Json file
    """
    jf['@context'] = {
       "@vocab": "https://glaciation-project.eu/MetadataReferenceModel#",
       "dpv": "https://w3id.org/dpv#"
    }
    temp_image_base64 = jf['image_base64']
    jf.pop('image_base64')
    expanded = jsonld.expand(jf)[0]
    expanded['image_base64'] = temp_image_base64
    #print(expanded)
    return expanded


# Define the base URL for the Apache NiFi endpoint
nifi_url = "http://semantification.validation/contentListener"

# Base directory where the datasets are located
base_dir = os.path.expanduser("~/DELL-UC/datasets")

# List of subdirectories (e.g., robot_0, robot_1, etc.)
subdirectories = ["robot_0", "robot_1", "robot_2", "robot_5", "robot_7"]


# Iterate through each subdirectory
for subdir in subdirectories:
    subdir_path = os.path.join(base_dir, subdir)
    
    # Iterate through each JSON file in the subdirectory
    TEST_MODE = False
    for filename in os.listdir(subdir_path):
        print(f'Processing file: {filename}')
        if filename.endswith(".json"):
            file_path = os.path.join(subdir_path, filename)
            
            # Read the JSON file
            with open(file_path, 'r') as file:
                #json_data = file.read()
                jf = json.load(file)
            
            json_data = json.dumps(expand_json(jf))
            print(json_data)

            # Send the JSON data to the Apache NiFi endpoint
            response = requests.post(nifi_url, data=json_data, headers={"Content-Type": "application/json"})
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"Successfully sent {filename} from {subdir} to Apache NiFi.")
            else:
                print(f"Failed to send {filename} from {subdir}. Status code: {response.status_code}")
        if TEST_MODE:
            break


print("All files processed.")

