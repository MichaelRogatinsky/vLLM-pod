# vLLM-pod - Qwen3-Coder-Next on RunPod Serverless

Deploy Qwen3-Coder-Next (or any compatible model) on RunPod Serverless with vLLM, featuring the latest dependency versions and proper tokenizer configuration.

## Features

- ✅ Latest vLLM (0.7.1+) and Transformers (4.46.0+) versions
- ✅ Optimized for Qwen3-Coder-Next with proper tokenizer support
- ✅ OpenAI-compatible API
- ✅ Supports up to 256K context length
- ✅ Easy deployment on RunPod Serverless
- ✅ Fixed tokenizer issues through `tokenizer_mode=auto`

## Quick Start

### Option 1: Deploy with Pre-built Docker Image

1. **Build the Docker image:**
   ```bash
   docker build -t your-username/vllm-qwen3-coder:latest .
   ```

2. **Push to Docker Hub:**
   ```bash
   docker push your-username/vllm-qwen3-coder:latest
   ```

3. **Deploy on RunPod:**
   - Go to [RunPod Serverless](https://www.runpod.io/console/serverless)
   - Create a new endpoint
   - Use your Docker image: `your-username/vllm-qwen3-coder:latest`
   - Set environment variables (see Configuration section)
   - Deploy!

### Option 2: Use Custom Model

You can deploy any vLLM-compatible model by setting the `MODEL_NAME` environment variable:

```bash
docker build -t your-username/vllm-custom:latest \
  --build-arg MODEL_NAME="your-org/your-model" .
```

## Configuration

Configure the worker using environment variables in RunPod:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `Qwen/Qwen3-Coder-Next` | Model repository ID or local path |
| `HF_TOKEN` | - | Hugging Face token for gated/private models |
| `MAX_MODEL_LEN` | `32768` | Maximum context length (up to 256k for Qwen3) |
| `GPU_MEMORY_UTILIZATION` | `0.90` | Fraction of GPU memory to use (0.0-1.0) |
| `TENSOR_PARALLEL_SIZE` | `1` | Number of GPUs for tensor parallelism |
| `QUANTIZATION` | - | Quantization method: awq, gptq, etc. |
| `MAX_NUM_SEQS` | `256` | Maximum concurrent sequences |
| `TRUST_REMOTE_CODE` | `true` | Trust remote code (required for Qwen) |
| `TOKENIZER_MODE` | `auto` | Tokenizer mode: auto or slow |

## Usage

### Python Example

```python
import requests
import os

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "your-endpoint-id"

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"

payload = {
    "input": {
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
        ],
        "sampling_params": {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9
        }
    }
}

headers = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### cURL Example

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
      ],
      "sampling_params": {
        "temperature": 0.7,
        "max_tokens": 2048
      }
    }
  }'
```

## Input Format

### Using Messages (Recommended)

```json
{
  "input": {
    "messages": [
      {"role": "system", "content": "System prompt"},
      {"role": "user", "content": "User message"}
    ],
    "sampling_params": {
      "temperature": 0.7,
      "max_tokens": 2048,
      "top_p": 0.9,
      "presence_penalty": 0.0,
      "frequency_penalty": 0.0
    }
  }
}
```

### Using Direct Prompt

```json
{
  "input": {
    "prompt": "Write a Python function to sort a list.",
    "sampling_params": {
      "temperature": 0.7,
      "max_tokens": 2048
    }
  }
}
```

## Output Format

```json
{
  "output": [
    {
      "text": "Generated text here...",
      "finish_reason": "stop",
      "tokens": 150
    }
  ],
  "model": "Qwen/Qwen3-Coder-Next"
}
```

## Hardware Requirements

### Recommended for Qwen3-Coder-Next

- **GPU**: NVIDIA A100 (40GB) or H100
- **Memory**: 40GB+ VRAM
- **Context**: 32K tokens fits comfortably in 40GB
- **For 256K context**: Multiple GPUs recommended

### Smaller Models

For smaller models or quantized versions:
- **GPU**: RTX 4090, A10, L40
- **Memory**: 24GB+ VRAM

## Troubleshooting

### Tokenizer Issues

If you encounter tokenizer errors:
1. Ensure `TOKENIZER_MODE=auto` is set
2. Verify `TRUST_REMOTE_CODE=true` is enabled
3. Check that transformers version is >= 4.46.0

### Out of Memory

If you hit OOM errors:
1. Reduce `MAX_MODEL_LEN` to 16384 or 8192
2. Lower `GPU_MEMORY_UTILIZATION` to 0.85
3. Reduce `MAX_NUM_SEQS` to 128 or 64
4. Consider quantization (set `QUANTIZATION=awq` or `gptq`)

### Slow Inference

To improve performance:
1. Increase `GPU_MEMORY_UTILIZATION` to 0.95
2. Use multiple GPUs with `TENSOR_PARALLEL_SIZE`
3. Enable flash attention (included in requirements)

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MODEL_NAME="Qwen/Qwen3-Coder-Next"
export MAX_MODEL_LEN=8192
export GPU_MEMORY_UTILIZATION=0.90

# Run the handler
python src/handler.py
```

### Building Custom Images

To build with a different model baked in:

```bash
docker build -t my-vllm-worker:latest \
  --build-arg MODEL_NAME="org/model-name" \
  --build-arg MAX_MODEL_LEN=16384 .
```

## License

MIT License - Feel free to use and modify for your needs.

## Credits

Based on [runpod-workers/worker-vllm](https://github.com/runpod-workers/worker-vllm) with updates for:
- Latest vLLM and Transformers versions
- Qwen3-Coder-Next optimization
- Fixed tokenizer configuration
- Simplified deployment

## Support

For issues and questions:
- Create an issue on GitHub
- Check RunPod documentation: https://docs.runpod.io/serverless/overview
- Check vLLM documentation: https://docs.vllm.ai/