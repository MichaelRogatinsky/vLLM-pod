# Deployment Guide for vLLM-pod

This guide will walk you through deploying vLLM-pod with Qwen3-Coder-Next on RunPod Serverless.

## Prerequisites

- Docker installed on your local machine
- Docker Hub account (or other container registry)
- RunPod account with API access
- Hugging Face account (for gated models, optional)

## Step 1: Build the Docker Image

### Option A: Using the build script (recommended)

```bash
# Build with default settings
./build.sh --username your-dockerhub-username

# Build with custom name and tag
./build.sh --username your-dockerhub-username --name my-vllm-worker --tag v1.0

# Build and push in one command
./build.sh --username your-dockerhub-username --push
```

### Option B: Manual Docker build

```bash
# Build the image
docker build -t your-dockerhub-username/vllm-qwen3-coder:latest .

# Push to Docker Hub
docker push your-dockerhub-username/vllm-qwen3-coder:latest
```

## Step 2: Test Locally (Optional)

Before deploying to RunPod, you can test the image locally if you have a GPU:

```bash
# Run with default model (Qwen3-Coder-Next)
docker run --gpus all \
  -e MODEL_NAME=Qwen/Qwen3-Coder-Next \
  -e MAX_MODEL_LEN=8192 \
  -e HF_TOKEN=your-hf-token \
  your-dockerhub-username/vllm-qwen3-coder:latest

# Or use docker-compose
docker-compose up
```

## Step 3: Deploy on RunPod Serverless

### 3.1 Create a New Serverless Endpoint

1. Go to [RunPod Console](https://www.runpod.io/console/serverless)
2. Click "New Endpoint" or "Create Endpoint"
3. Fill in the basic information:
   - **Name**: `vllm-qwen3-coder` (or your preferred name)
   - **Description**: `Qwen3-Coder-Next with latest vLLM`

### 3.2 Configure Container Image

In the Container Configuration section:

- **Container Image**: `your-dockerhub-username/vllm-qwen3-coder:latest`
- **Container Registry Credentials**: Leave empty if using a public image

### 3.3 Set Environment Variables

Add these environment variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `MODEL_NAME` | `Qwen/Qwen3-Coder-Next` | Or your custom model |
| `MAX_MODEL_LEN` | `32768` | Start with 32K, increase if needed |
| `GPU_MEMORY_UTILIZATION` | `0.90` | Adjust based on your GPU |
| `TENSOR_PARALLEL_SIZE` | `1` | Set to number of GPUs you want to use |
| `TRUST_REMOTE_CODE` | `true` | Required for Qwen models |
| `TOKENIZER_MODE` | `auto` | Fixes tokenizer issues |
| `HF_TOKEN` | `your-token` | Only if using gated/private models |

### 3.4 Configure GPU and Resources

- **GPU Type**: Select A100 (40GB) or H100 for best performance
- **GPUs Per Worker**: 1 (or more if using tensor parallelism)
- **Worker Count**: Start with 0 (autoscaling)
- **Max Workers**: 3-5 depending on your needs
- **Idle Timeout**: 5 seconds (for cost efficiency)

### 3.5 Advanced Settings (Optional)

- **Execution Timeout**: 300 seconds (5 minutes)
- **Container Disk**: 20 GB (default is usually enough)
- **Volume Mount**: Optional for model caching

## Step 4: Deploy and Test

1. Click "Deploy" at the bottom of the page
2. Wait for the endpoint to become active (usually 2-5 minutes)
3. Copy your Endpoint ID from the endpoint page

### Test Your Endpoint

See examples in the [examples/](../examples/) directory.

## Step 5: Monitor and Scale

### Monitoring

1. Go to your endpoint page on RunPod
2. Click on "Metrics" to see:
   - Request count
   - Average execution time
   - Error rate
   - Active workers

### Scaling

- **Increase Max Workers**: If you're hitting capacity
- **Increase GPU Count**: Set `TENSOR_PARALLEL_SIZE=2` or higher
- **Reduce Idle Timeout**: For consistently high traffic
- **Increase Context Length**: Adjust `MAX_MODEL_LEN` if needed

## Troubleshooting

### Issue: Workers Not Starting

**Solution:**
- Check Docker image is accessible
- Verify environment variables are set correctly
- Check RunPod logs for detailed error messages

### Issue: Out of Memory Errors

**Solutions:**
1. Reduce `MAX_MODEL_LEN` from 32768 to 16384 or 8192
2. Lower `GPU_MEMORY_UTILIZATION` to 0.85
3. Reduce `MAX_NUM_SEQS` to 128 or 64
4. Use quantization: Set `QUANTIZATION=awq`

### Issue: Slow Cold Starts

**Solutions:**
1. Set minimum workers to 1 instead of 0
2. Increase idle timeout to 60 seconds
3. Use a smaller model for faster loading

### Issue: Tokenizer Errors

**Solutions:**
1. Ensure `TOKENIZER_MODE=auto` is set
2. Verify `TRUST_REMOTE_CODE=true` is enabled
3. Check your transformers version is >= 4.46.0

## Cost Optimization

1. **Use Autoscaling**: Set min workers to 0, max to your needs
2. **Short Idle Timeout**: 5 seconds for serverless workloads
3. **Right-Size GPU**: Use A10 for smaller models, A100 for Qwen3-Coder-Next
4. **Reduce Context Length**: Lower `MAX_MODEL_LEN` if you don't need 32K
5. **Batch Requests**: Group multiple requests when possible

## Additional Resources

- [RunPod Serverless Docs](https://docs.runpod.io/serverless/overview)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Qwen3-Coder-Next Model Card](https://huggingface.co/Qwen/Qwen3-Coder-Next)
