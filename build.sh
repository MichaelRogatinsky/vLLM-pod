#!/bin/bash
# Build script for vLLM-pod Docker image

set -e

# Default values
IMAGE_NAME="${IMAGE_NAME:-vllm-qwen3-coder}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKER_USERNAME="${DOCKER_USERNAME:-yourname}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --username)
            DOCKER_USERNAME="$2"
            shift 2
            ;;
        --push)
            PUSH_IMAGE=true
            shift
            ;;
        --help)
            echo "Usage: ./build.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --name        Image name (default: vllm-qwen3-coder)"
            echo "  --tag         Image tag (default: latest)"
            echo "  --username    Docker Hub username (default: yourname)"
            echo "  --push        Push image to Docker Hub after build"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "=================================================="
echo "Building vLLM-pod Docker Image"
echo "=================================================="
echo "Image: ${FULL_IMAGE_NAME}"
echo ""

# Build the image
echo "Building Docker image..."
docker build -t "${FULL_IMAGE_NAME}" .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Image: ${FULL_IMAGE_NAME}"
    
    if [ "$PUSH_IMAGE" = true ]; then
        echo ""
        echo "Pushing image to Docker Hub..."
        docker push "${FULL_IMAGE_NAME}"
        
        if [ $? -eq 0 ]; then
            echo "✅ Push successful!"
        else
            echo "❌ Push failed!"
            exit 1
        fi
    fi
    
    echo ""
    echo "=================================================="
    echo "Next steps:"
    echo "=================================================="
    echo "1. Test locally:"
    echo "   docker run --gpus all -e MODEL_NAME=Qwen/Qwen3-Coder-Next ${FULL_IMAGE_NAME}"
    echo ""
    echo "2. Push to Docker Hub:"
    echo "   docker push ${FULL_IMAGE_NAME}"
    echo ""
    echo "3. Deploy on RunPod:"
    echo "   - Go to https://www.runpod.io/console/serverless"
    echo "   - Create new endpoint"
    echo "   - Use image: ${FULL_IMAGE_NAME}"
    echo "=================================================="
else
    echo "❌ Build failed!"
    exit 1
fi
