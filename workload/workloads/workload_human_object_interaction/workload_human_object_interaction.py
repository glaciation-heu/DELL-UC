import os
import argparse
import requests
from collections import defaultdict

# Define function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the workload with configurable metadata service URL")
    parser.add_argument(
        "--url",
        type=str,
        default=None,  # Default is None; will fall back to environment variable or hardcoded value later
        help="Metadata service URL"
    )
    return parser.parse_args()

# List of potentially dangerous objects
DANGEROUS_OBJECTS = ["chainsaw", "drill", "forklift"]

# Step 1: Construct the SPARQL Query
def construct_sparql_query():
    sparql_query = """
    PREFIX ex: <http://example.org/>
    SELECT ?worker ?object ?zone ?timestamp
    WHERE {
      ?detection ex:workerDetected ?worker ;
                 ex:objectDetected ?object ;
                 ex:zone ?zone ;
                 ex:timestamp ?timestamp .
    }
    """
    return sparql_query

# Step 2: Submit the SPARQL query to the metadata service using GET request
def submit_sparql_query(sparql_query, metadata_service_url):
    try:
        response = requests.get(metadata_service_url, params={'query': sparql_query}, headers={'Accept': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying metadata service: {e}")
        return None

# Step 3: Process the response data to analyze worker-object interactions
def process_response(data):
    worker_interactions = defaultdict(lambda: defaultdict(int))
    unsafe_interactions = []

    for result in data.get("results", {}).get("bindings", []):
        worker = result.get("worker", {}).get("value")
        obj = result.get("object", {}).get("value")
        zone = result.get("zone", {}).get("value")

        if worker and obj:
            # Track the frequency of interactions between workers and objects
            worker_interactions[worker][obj] += 1

            # Detect unsafe interactions if workers are near dangerous objects
            if obj in DANGEROUS_OBJECTS:
                unsafe_interactions.append({
                    "worker": worker,
                    "object": obj,
                    "zone": zone,
                    "issue": f"Worker '{worker}' is interacting with dangerous object '{obj}' in zone '{zone}'"
                })

    return worker_interactions, unsafe_interactions

# Step 4: Generate insights and print interaction and safety metrics
def generate_insights(worker_interactions, unsafe_interactions):
    print("---- Worker-Object Interaction Frequency ----")
    for worker, objects in worker_interactions.items():
        print(f"Worker {worker}:")
        for obj, count in objects.items():
            print(f"  {obj}: {count} interactions")

    print("\n---- Unsafe Interactions ----")
    if unsafe_interactions:
        for interaction in unsafe_interactions:
            print(f"Unsafe Interaction: {interaction['issue']}")
    else:
        print("No unsafe interactions detected.")

# Main function to run the workload
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Check if the command-line argument is provided, then check environment variable, then fallback to default
    metadata_service_url = args.url or os.getenv("METADATA_SERVICE_URL", "http://metadata.uc2/api/v0/graph")

    print(f"Using Metadata Service URL: {metadata_service_url}")

    # Step 1: Construct the SPARQL query
    sparql_query = construct_sparql_query()

    # Step 2: Submit the query to the metadata service and get the response
    response_data = submit_sparql_query(sparql_query, metadata_service_url)

    if response_data:
        # Step 3: Process the response data to analyze worker-object interactions
        worker_interactions, unsafe_interactions = process_response(response_data)

        # Step 4: Generate insights and print the results
        generate_insights(worker_interactions, unsafe_interactions)

if __name__ == "__main__":
    main()

