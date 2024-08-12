import os
import cv2
import torch
import json
import base64
from itertools import cycle
from pathlib import Path
from PIL import Image, ImageFile, ExifTags

# Function to load YOLOv5 model
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

# Function to perform object detection on an image
def detect_objects(model, img_path):
    results = model(img_path)
    return results

# Function to extract EXIF metadata from an image
def extract_metadata(img_path):
    metadata = {}
    try:
        image = Image.open(img_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                metadata[tag_name] = value
    except Exception as e:
        print(f"Error extracting metadata from image {img_path}: {e}")
    
    return metadata

# Function to clear existing JSON files from the output directories
def clear_json_files(base_dir):
    cameras = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for camera in cameras:
        camera_number = camera.split('_')[-1]
        output_dir = os.path.join(base_dir, f'robot_{camera_number}')
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(output_dir, filename)
                    os.remove(file_path)

# Function to encode image to base64 string
def encode_image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define lists of possible DPV values
dpv_purposes = ["Security monitoring", "Research and Development", "Service Personalization"]
dpv_data_controllers = ["Organization XYZ", "Research Lab ABC", "Service Provider 123"]
dpv_legal_bases = ["Legitimate Interest", "Consent", "Legal Obligation"]
dpv_technical_measures = [
    {"dpv:Encryption": "AES-256", "dpv:AccessControl": "Role-based access", "dpv:DataMinimization": "Only capturing images during specific hours"},
    {"dpv:Encryption": "AES-128", "dpv:AccessControl": "Password protected", "dpv:DataMinimization": "Capturing minimal necessary data"},
    {"dpv:Encryption": "RSA", "dpv:AccessControl": "Biometric", "dpv:DataMinimization": "Recording only necessary parts"}
]
dpv_rights = [["Access", "Erasure"], ["Access", "Rectification"], ["Access", "Portability"]]
dpv_risks = [["Unauthorized access", "Data breach"], ["Data leakage", "Loss of data"], ["System malfunction", "Data corruption"]]

# Define lists of possible ODRL values
odrl_permissions = ["use", "reproduce", "distribute"]
odrl_prohibitions = ["modify", "delete", "sell"]
odrl_duties = ["attribution", "shareAlike", "source"]

# Create cycles for DPV and ODRL values
dpv_purpose_cycle = cycle(dpv_purposes)
dpv_data_controller_cycle = cycle(dpv_data_controllers)
dpv_legal_basis_cycle = cycle(dpv_legal_bases)
dpv_technical_measures_cycle = cycle(dpv_technical_measures)
dpv_rights_cycle = cycle(dpv_rights)
dpv_risks_cycle = cycle(dpv_risks)
odrl_permission_cycle = cycle(odrl_permissions)
odrl_prohibition_cycle = cycle(odrl_prohibitions)
odrl_duty_cycle = cycle(odrl_duties)

# Function to process the images in a directory and output JSON
def process_directory(base_dir):
    model = load_model()

    cameras = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for camera in cameras:
        image_dir = os.path.join(base_dir, camera, 'images')
        if os.path.exists(image_dir):
            # Create the output directory for the current camera
            camera_number = camera.split('_')[-1]
            robot_name = f'robot_{camera_number}'
            output_dir = os.path.join(base_dir, robot_name)
            os.makedirs(output_dir, exist_ok=True)

            # Assign DPV and ODRL values for this robot
            dpv_purpose = next(dpv_purpose_cycle)
            dpv_data_controller = next(dpv_data_controller_cycle)
            dpv_legal_basis = next(dpv_legal_basis_cycle)
            dpv_technical_measures = next(dpv_technical_measures_cycle)
            dpv_rights = next(dpv_rights_cycle)
            dpv_risks = next(dpv_risks_cycle)
            odrl_permission = next(odrl_permission_cycle)
            odrl_prohibition = next(odrl_prohibition_cycle)
            odrl_duty = next(odrl_duty_cycle)

            images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
            for image in images:
                img_path = os.path.join(image_dir, image)
                try:
                    # Load and verify the image
                    ImageFile.LOAD_TRUNCATED_IMAGES = True
                    with Image.open(img_path) as img:
                        img.verify()

                    # Perform object detection
                    results = detect_objects(model, img_path)

                    # Extract and add metadata
                    metadata = extract_metadata(img_path)
                    metadata.update({
                        "SensorAspectRatio": "8:5",
                        "Format": "10-bit RAW",
                        "FNumber": "f/2.0",
                        "FocalLength": "1.93mm",
                        "FilterType": "None",
                        "Focus": "Fixed",
                        "ShutterType": "Global shutter",
                        "SignalInterface": "MIPI CSI-2, 2X lanes",
                        "HorizontalFieldOfView": "91.2°",
                        "VerticalFieldOfView": "65.5°",
                        "DiagonalFieldOfView": "100.6°",
                        "Distortion": "<=1.5%",
                        "dpv:Purpose": dpv_purpose,
                        "dpv:DataController": dpv_data_controller,
                        "dpv:LegalBasis": dpv_legal_basis,
                        "dpv:TechnicalAndOrganisationalMeasures": dpv_technical_measures,
                        "dpv:Rights": dpv_rights,
                        "dpv:Risks": dpv_risks,
                        "odrl:Policy": {
                            "uid": f"http://example.com/policy/{camera_number}",
                            "permission": [{"target": "image", "action": odrl_permission}],
                            "prohibition": [{"target": "image", "action": odrl_prohibition}],
                            "duty": [{"action": odrl_duty}]
                        }
                    })

                    # Encode image to base64
                    image_base64 = encode_image_to_base64(img_path)

                    image_data = {
                        "metadata": metadata,
                        "detections": [],
                        "image_base64": image_base64
                    }

                    # Add detection results
                    for result in results.xyxy[0]:
                        x1, y1, x2, y2, conf, cls = result[:6].tolist()
                        class_name = model.names[int(cls)]
                        image_data["detections"].append({
                            "class": int(cls),
                            "name": class_name,
                            "confidence": conf,
                            "bounding_box": {
                                "x1": x1,
                                "y1": y1,
                                "x2": x2,
                                "y2": y2
                            }
                        })
                    
                    # Write the results to a JSON file
                    output_file = os.path.join(output_dir, f'{Path(image).stem}.json')
                    with open(output_file, 'w') as json_file:
                        json.dump(image_data, json_file, indent=4)

                except (OSError, IOError) as e:
                    print(f"Error processing image {img_path}: {e}")

# Define the base directory containing the camera directories
base_dir = 'scenario_1_with_dist_LVL_0'

# Clear existing JSON files
clear_json_files(base_dir)

# Process the directory and output the results to JSON
process_directory(base_dir)

