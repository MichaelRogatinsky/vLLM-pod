# Quick Start Guide

Get your Qwen3-Coder-Next endpoint running on RunPod in minutes!

## 1. Build & Push (5 minutes)

```bash
# Clone the repository
git clone https://github.com/MichaelRogatinsky/vLLM-pod.git
cd vLLM-pod

# Build and push to Docker Hub
./build.sh --username YOUR_DOCKERHUB_USERNAME --push
```

## 2. Deploy on RunPod (2 minutes)

1. Go to [RunPod Serverless Console](https://www.runpod.io/console/serverless)
2. Click "New Endpoint"
3. Configure:
   - **Name**: `qwen3-coder`
   - **Image**: `YOUR_DOCKERHUB_USERNAME/vllm-qwen3-coder:latest`
   - **GPU**: A100 (40GB) or H100
   - **Environment Variables**:
     ```
     MODEL_NAME=Qwen/Qwen3-Coder-Next
     MAX_MODEL_LEN=32768
     GPU_MEMORY_UTILIZATION=0.90
     TOKENIZER_MODE=auto
     TRUST_REMOTE_CODE=true
     ```
4. Click "Deploy"
5. Wait 2-5 minutes for initialization

## 3. Test Your Endpoint (1 minute)

### Python

```python
import requests
import os

RUNPOD_API_KEY = "YOUR_API_KEY"
ENDPOINT_ID = "YOUR_ENDPOINT_ID"

response = requests.post(
    f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
    headers={
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "input": {
            "messages": [
                {"role": "user", "content": "Write a Python hello world function"}
            ],
            "sampling_params": {
                "temperature": 0.7,
                "max_tokens": 512
            }
        }
    }
)

print(response.json())
```

### cURL

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "Write a Python hello world function"}
      ],
      "sampling_params": {
        "temperature": 0.7,
        "max_tokens": 512
      }
    }
  }'
```

## That's it! 🎉

Your Qwen3-Coder-Next endpoint is now live and ready to use.

## Next Steps

- Check [examples/](examples/) for more usage patterns
- Read [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed configuration
- See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the system

## Troubleshooting

### Out of Memory?
Reduce `MAX_MODEL_LEN` to `16384` or `8192`

### Slow startup?
First request takes ~30s to load the model. Subsequent requests are fast.

### Still having issues?
Check the full [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) troubleshooting section.

## Key Features

✅ Latest vLLM (0.7.1+) and Transformers (4.46.0+)  
✅ Fixed tokenizer issues with `TOKENIZER_MODE=auto`  
✅ Supports up to 256K context (configurable)  
✅ OpenAI-compatible API  
✅ Automatic chat template handling  
✅ Multi-GPU support via tensor parallelism  
✅ Production-ready with comprehensive docs  

## Support

- Issues: [GitHub Issues](https://github.com/MichaelRogatinsky/vLLM-pod/issues)
- RunPod Docs: [docs.runpod.io](https://docs.runpod.io/)
- vLLM Docs: [docs.vllm.ai](https://docs.vllm.ai/)
