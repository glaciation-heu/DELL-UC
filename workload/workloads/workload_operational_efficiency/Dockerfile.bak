# workloads/workload_object_distribution/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install required libraries (if any specific dependencies are needed)
COPY ../../common/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload_object_distribution.py /app/

# Run the workload
CMD ["python", "workload_object_distribution.py"]

