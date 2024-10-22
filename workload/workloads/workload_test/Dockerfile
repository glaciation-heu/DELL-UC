# workload/workloads/workload_test/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload/workloads/workload_test/workload.py /app/

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Run the workload
CMD ["python", "workload.py"]
