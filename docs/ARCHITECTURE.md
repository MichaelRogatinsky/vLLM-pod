# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         RunPod Serverless                        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Docker Container                        │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐     │  │
│  │  │              handler.py                         │     │  │
│  │  │   - Receives RunPod job input                   │     │  │
│  │  │   - Routes requests to vLLM engine              │     │  │
│  │  │   - Returns formatted responses                 │     │  │
│  │  └──────────────────┬───────────────────────────────┘     │  │
│  │                     │                                      │  │
│  │                     ▼                                      │  │
│  │  ┌──────────────────────────────────────────────────┐     │  │
│  │  │           vllm_engine.py                        │     │  │
│  │  │   - Initializes vLLM with Qwen3-Coder-Next     │     │  │
│  │  │   - Handles tokenizer configuration             │     │  │
│  │  │   - Applies chat templates                      │     │  │
│  │  │   - Manages inference with sampling params      │     │  │
│  │  └──────────────────┬───────────────────────────────┘     │  │
│  │                     │                                      │  │
│  │                     ▼                                      │  │
│  │  ┌──────────────────────────────────────────────────┐     │  │
│  │  │              vLLM Engine                        │     │  │
│  │  │   - LLM inference engine                        │     │  │
│  │  │   - GPU-accelerated generation                  │     │  │
│  │  │   - Tokenizer (auto mode)                       │     │  │
│  │  │   - Trust remote code: enabled                  │     │  │
│  │  └──────────────────┬───────────────────────────────┘     │  │
│  │                     │                                      │  │
│  │                     ▼                                      │  │
│  │  ┌──────────────────────────────────────────────────┐     │  │
│  │  │         Qwen/Qwen3-Coder-Next Model             │     │  │
│  │  │   - 80B parameters (3B active)                  │     │  │
│  │  │   - 256K context window                         │     │  │
│  │  │   - Loaded from Hugging Face Hub                │     │  │
│  │  └──────────────────────────────────────────────────┘     │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ API Requests
                              ▼
                    ┌──────────────────┐
                    │  Client (User)   │
                    │  - Python SDK    │
                    │  - cURL          │
                    │  - REST API      │
                    └──────────────────┘
```

## Request Flow

```
1. Client Request
   └─> RunPod API Endpoint (https://api.runpod.ai/v2/{endpoint_id}/runsync)
       └─> handler.py receives job input
           └─> vllm_engine.py processes request
               └─> Tokenizer applies chat template (if messages provided)
                   └─> vLLM engine generates text
                       └─> Response formatted and returned
                           └─> Client receives output
```

## Key Components

### 1. Dockerfile
- **Base**: CUDA 12.1.1 + cuDNN 8 + Ubuntu 22.04
- **Python**: 3.11
- **Dependencies**: vLLM 0.7.1+, Transformers 4.46.0+, PyTorch 2.5.0+
- **Configuration**: Environment variables for all settings

### 2. Handler (handler.py)
- Entry point for RunPod serverless
- Receives job input in RunPod format
- Routes to vLLM engine
- Returns formatted responses

### 3. vLLM Engine (vllm_engine.py)
- Initializes vLLM with Qwen3-Coder-Next
- Configures tokenizer (mode=auto, trust_remote_code=true)
- Handles chat template application
- Manages sampling parameters
- Performs inference

### 4. Configuration Files

#### worker-config.json
- RunPod worker schema
- Environment variable definitions
- Default values and descriptions

#### requirements.txt
- Python dependencies with version constraints
- Latest compatible versions specified

#### docker-compose.yml
- Local testing configuration
- GPU passthrough
- Volume mounts for model caching

## Data Flow

### Input Format

```json
{
  "input": {
    "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ],
    "sampling_params": {
      "temperature": 0.7,
      "max_tokens": 2048,
      "top_p": 0.9
    }
  }
}
```

### Output Format

```json
{
  "output": [
    {
      "text": "Generated text...",
      "finish_reason": "stop",
      "tokens": 150
    }
  ],
  "model": "Qwen/Qwen3-Coder-Next"
}
```

## Tokenizer Configuration

### The Fix

The tokenizer issues were resolved by:

1. **TOKENIZER_MODE=auto**
   - Lets vLLM automatically detect and configure the tokenizer
   - Handles Qwen3-specific tokenization correctly

2. **TRUST_REMOTE_CODE=true**
   - Required for Qwen models
   - Allows custom tokenizer implementations

3. **Latest Transformers (4.46.0+)**
   - Includes Qwen3 support
   - Proper chat template handling

### Tokenizer Flow

```
Input (messages) 
    └─> Check for chat template
        └─> Apply tokenizer.apply_chat_template()
            └─> Generate tokenized prompt
                └─> vLLM inference
                    └─> Decode output
                        └─> Return text
```

## Deployment Architecture

```
Developer Machine
    └─> docker build (creates image)
        └─> docker push (to Docker Hub)
            └─> RunPod Serverless
                └─> Pulls image
                    └─> Creates workers with GPUs
                        └─> Loads model from HuggingFace
                            └─> Ready to serve requests
```

## Resource Usage

### GPU Memory Breakdown (A100 40GB example)

```
Model Weights:       ~25-30 GB (FP16)
KV Cache (32K ctx):  ~8-10 GB
vLLM Overhead:       ~1-2 GB
System Reserve:      ~1 GB
─────────────────────────────
Total:               ~35-43 GB (fits in 40GB with 0.90 utilization)
```

### Scalability

- **Horizontal**: Multiple workers (RunPod autoscaling)
- **Vertical**: Tensor parallelism across GPUs (TENSOR_PARALLEL_SIZE)
- **Context**: Configurable from 8K to 256K tokens

## Environment Variables

Critical settings:

```bash
MODEL_NAME=Qwen/Qwen3-Coder-Next    # Model to load
MAX_MODEL_LEN=32768                  # Context window
GPU_MEMORY_UTILIZATION=0.90          # GPU memory fraction
TOKENIZER_MODE=auto                  # Fix for tokenizer
TRUST_REMOTE_CODE=true               # Required for Qwen
```

## Security Considerations

1. **Trust Remote Code**: Required but validated by HuggingFace
2. **API Keys**: Use environment variables, never hardcode
3. **Container Security**: Base NVIDIA image with minimal packages
4. **Model Validation**: Models downloaded from official HuggingFace repos

## Performance Optimizations

1. **Flash Attention 2**: Included in dependencies
2. **Tensor Parallelism**: Multi-GPU support
3. **GPU Memory Utilization**: Configurable (default 0.90)
4. **Batch Processing**: MAX_NUM_SEQS controls concurrent requests
5. **Model Caching**: HuggingFace cache can be volume-mounted
