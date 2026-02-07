# Base image with CUDA 12.1
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    PATH="${CUDA_HOME}/bin:${PATH}" \
    LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Install PyTorch first (required for flash-attn compilation)
RUN pip install --no-cache-dir torch>=2.5.0

# Install flash-attn separately (requires torch)
RUN pip install --no-cache-dir flash-attn>=2.7.0

# Install remaining dependencies
RUN pip install --no-cache-dir \
    vllm>=0.15.1 \
    transformers>=5.1.0 \
    runpod>=1.7.0 \
    huggingface_hub>=0.26.0 \
    tokenizers>=0.20.0 \
    fastapi>=0.115.0 \
    uvicorn>=0.32.0 \
    pydantic>=2.9.0 \
    aiohttp>=3.11.0 \
    numpy>=1.26.0 \
    requests>=2.32.0

# Copy application code
COPY src/ /app/src/

# Set default model (can be overridden with environment variable)
ENV MODEL_NAME="Qwen/Qwen3-Coder-Next" \
    MAX_MODEL_LEN=32768 \
    GPU_MEMORY_UTILIZATION=0.90 \
    TENSOR_PARALLEL_SIZE=1 \
    TRUST_REMOTE_CODE=true \
    QUANTIZATION="" \
    MAX_NUM_SEQS=256 \
    TOKENIZER_MODE=auto

# Run the handler
CMD ["python3", "-u", "/app/src/handler.py"]
