import os
import requests

# Define the base URL for the Apache NiFi endpoint
nifi_url = "http://semantification.uc2/contentListener"

# Base directory where the datasets are located
base_dir = os.path.expanduser("~/DELL-UC/datasets")

# List of subdirectories (e.g., robot_0, robot_1, etc.)
subdirectories = ["robot_0", "robot_1", "robot_2", "robot_5", "robot_7"]

# Iterate through each subdirectory
for subdir in subdirectories:
    subdir_path = os.path.join(base_dir, subdir)
    
    # Iterate through each JSON file in the subdirectory
    for filename in os.listdir(subdir_path):
        if filename.endswith(".json"):
            file_path = os.path.join(subdir_path, filename)
            
            # Read the JSON file
            with open(file_path, 'r') as file:
                json_data = file.read()
            
            # Send the JSON data to the Apache NiFi endpoint
            response = requests.post(nifi_url, data=json_data, headers={"Content-Type": "application/json"})
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"Successfully sent {filename} from {subdir} to Apache NiFi.")
            else:
                print(f"Failed to send {filename} from {subdir}. Status code: {response.status_code}")

print("All files processed.")

