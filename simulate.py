import argparse
import base64
import requests
import json
import glob

def get_test_sample():
    # SET UP mock JSON file
    TEST = {
    
        "timestamp": "2024-04-09T11:03:24.870875",
        "frame": "<base 64 encoded jpg in here>",
        "frame_resolution": "640x480",
        "robot_id" : "robot_01",
        "camera_id": "Camera_01",
        "detections": [
            {
                "label": "tvmonitor",
                "confidence": 0.6650710105895996,
                "bounding_box": {
                    "x": 241,
                    "y": 135,
                    "width": 245,
                    "height": 188
                }
            },
            {
                "label": "person",
                "confidence": 0.7242302894592285,
                "bounding_box": {
                    "x": 12,
                    "y": 236,
                    "width": 291,
                    "height": 238
                }
            },
            {
                "label": "cell phone",
                "confidence": 0.9596779942512512,
                "bounding_box": {
                    "x": 147,
                    "y": 22,
                    "width": 146,
                    "height": 206
                }
            }
        ],
        "num_detections": 3
    }
    
    with open('./input/test.jpg', 'rb') as image_file:
        encoded_str = base64.b64encode(image_file.read()).decode('utf-8')
        print(encoded_str)
        TEST['frame'] = encoded_str

    return TEST


def process_json(json_file: str, robotId, repeat=1, sleep=5000):
    """ Read JSON and do HTTP POST request to NiFi """
    
    json_file['robot_id'] = 'robot_' + robotId
    json_file['camera_id'] = 'r' + robotId + '_' + 'c' + json_file['camera_id'].split('_')[1]

    # print(json_file)

    # POST
    r = requests.post(
        'http://localhost:8889/contentListener',
        json=json_file
    )
    print(r.status_code)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate streaming data from robot, seding a set of JSON files to Apache NiFi')
    parser.add_argument('-t', '--test', action='store_true', help='test with one sample')
    parser.add_argument('--robotId', default='01', help='change robotId before adding data')
    args = parser.parse_args()

    if args.test:
        test_sample = get_test_sample()
        process_json(test_sample, robotId=args.robotId)
    else:
        for idx, i in enumerate(glob.glob('../json_files/data_files/*')):
            print(f'Processing {idx, i}')
            # Test one json file
            with open(i) as f:
                doc = json.load(f)
                process_json(doc, robotId=args.robotId)
