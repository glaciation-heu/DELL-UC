# workloads/workload_object_distribution/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload/workloads/workload_object_distribution/workload_object_distribution.py /app/

# Run the workload
CMD ["python", "workload_object_distribution.py", "--url", "http://metadata-service.dkg-engine.svc.cluster.local/api/v0/graph"]

