# Use the official NVIDIA CUDA base image
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /training

# Install Python and build tools
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# This container usually runs a script and then exits
ENTRYPOINT ["python3", "train_cascade.py"]
