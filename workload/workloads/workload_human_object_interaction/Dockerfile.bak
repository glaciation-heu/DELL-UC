# workloads/workload_human_object_interaction/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install required libraries (if any dependencies are needed)
COPY ../../common/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy workload script
COPY workload_human_object_interaction.py /app/

# Run the workload
CMD ["python", "workload_human_object_interaction.py"]

