# workloads/workload_object_distribution/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install required libraries (if any specific dependencies are needed)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload/workloads/workload_operational_efficiency/workload_operational_efficiency.py /app/

# Run the workload
CMD ["python", "workload_operational_efficiency.py", "--url", "http://metadata-service.dkg-engine.svc.cluster.local/api/v0/graph"]

