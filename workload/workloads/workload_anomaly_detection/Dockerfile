# workloads/workload_anomaly_detection/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install required libraries (if any dependencies are needed)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload/workloads/workload_anomaly_detection/workload_anomaly_detection.py /app/

# Run the workload
CMD ["python", "workload_anomaly_detection.py", "--url", "http://metadata-service.dkg-engine.svc.cluster.local/api/v0/graph"]

