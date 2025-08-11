FROM jupyter/all-spark-notebook:latest

# Switch to root for installations
USER root

# Update and install additional system dependencies if needed
RUN apt-get update && \
    apt-get install -y wget curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER ${NB_UID}

# Copy requirements and install Python dependencies in stages
COPY requirements.txt /tmp/requirements.txt

# Install dependencies in stages to handle potential conflicts
# First install PyTorch with CPU-only version to avoid CUDA issues
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then install remaining requirements
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app files to the work directory
COPY app/ /home/jovyan/work/

EXPOSE 8888
