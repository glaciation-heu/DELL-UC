# Base image with Python 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all project files to the container
COPY . /app

# Install system dependencies (for libraries like scikit-learn and matplotlib)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port for monitoring (if applicable)
EXPOSE 5000

# To suppress TensorFlow warnings
ENV TF_ENABLE_ONEDNN_OPTS=0

# Command to run the OpenTraj workload script
CMD ["python", "Dell-UC2_OpenTraj_workload.py"]

