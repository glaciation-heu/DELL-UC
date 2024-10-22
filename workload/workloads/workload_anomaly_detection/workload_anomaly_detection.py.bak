import requests
from collections import defaultdict

# Define the URL for the metadata service's SPARQL endpoint
METADATA_SERVICE_URL = "http://metadataservice.validation/api/v0/graph"

# List of known restricted zones or areas where certain objects should not appear
RESTRICTED_ZONES = {
    "ZoneA": ["ladder", "vehicle"],  # Example: ladder and vehicle should not be in ZoneA
    "ZoneB": ["medical_equipment"],   # Medical equipment should not be in ZoneB
    # Add more restricted zones and restricted objects as needed
}

# Step 1: Construct the SPARQL Query
def construct_sparql_query():
    sparql_query = """
    PREFIX ex: <http://example.org/>
    SELECT ?object ?zone ?timestamp
    WHERE {
      ?detection ex:objectDetected ?object ;
                 ex:zone ?zone ;
                 ex:timestamp ?timestamp .
    }
    """
    return sparql_query

# Step 2: Submit the SPARQL query to the metadata service using GET request
def submit_sparql_query(sparql_query):
    try:
        response = requests.get(METADATA_SERVICE_URL, params={'query': sparql_query}, headers={'Accept': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying metadata service: {e}")
        return None

# Step 3: Process the response data to detect anomalies
def process_response(data):
    anomalies = []
    object_frequency_by_zone = defaultdict(lambda: defaultdict(int))

    for result in data.get("results", {}).get("bindings", []):
        obj = result.get("object", {}).get("value")
        zone = result.get("zone", {}).get("value")

        if obj and zone:
            # Count object frequency in each zone
            object_frequency_by_zone[zone][obj] += 1

            # Check if the object is in a restricted zone
            if zone in RESTRICTED_ZONES and obj in RESTRICTED_ZONES[zone]:
                anomalies.append({
                    "object": obj,
                    "zone": zone,
                    "issue": f"Object '{obj}' detected in restricted zone '{zone}'"
                })

    return anomalies, object_frequency_by_zone

# Step 4: Generate insights and print anomaly detection metrics
def generate_insights(anomalies, object_frequency_by_zone):
    print("---- Anomaly Detection ----")
    if anomalies:
        for anomaly in anomalies:
            print(f"Anomaly: {anomaly['issue']}")
    else:
        print("No anomalies detected.")

    print("\n---- Object Frequency by Zone ----")
    for zone, objects in object_frequency_by_zone.items():
        print(f"Zone {zone}:")
        for obj, count in objects.items():
            print(f"  {obj}: {count} detections")

# Main function to run the workload
def main():
    # Step 1: Construct the SPARQL query
    sparql_query = construct_sparql_query()

    # Step 2: Submit the query to the metadata service and get the response
    response_data = submit_sparql_query(sparql_query)

    if response_data:
        # Step 3: Process the response data to detect anomalies
        anomalies, object_frequency_by_zone = process_response(response_data)

        # Step 4: Generate insights and print the results
        generate_insights(anomalies, object_frequency_by_zone)

if __name__ == "__main__":
    main()

