#!/bin/bash
# Example cURL requests for vLLM-pod

# Configuration
RUNPOD_API_KEY="${RUNPOD_API_KEY:-your-api-key-here}"
ENDPOINT_ID="${ENDPOINT_ID:-your-endpoint-id}"

if [ "$RUNPOD_API_KEY" = "your-api-key-here" ] || [ "$ENDPOINT_ID" = "your-endpoint-id" ]; then
    echo "⚠️  Please set RUNPOD_API_KEY and ENDPOINT_ID environment variables"
    echo ""
    echo "Example:"
    echo "  export RUNPOD_API_KEY='your-actual-key'"
    echo "  export ENDPOINT_ID='your-endpoint-id'"
    echo "  ./example_curl.sh"
    exit 1
fi

API_URL="https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync"

echo "=================================================="
echo "vLLM-pod cURL Examples"
echo "=================================================="
echo ""

# Example 1: Simple code generation with messages
echo "Example 1: Code Generation with Messages"
echo "--------------------------------------------------"
curl -X POST "${API_URL}" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to reverse a string."}
      ],
      "sampling_params": {
        "temperature": 0.7,
        "max_tokens": 512
      }
    }
  }'

echo ""
echo ""

# Example 2: Direct prompt
echo "Example 2: Direct Prompt"
echo "--------------------------------------------------"
curl -X POST "${API_URL}" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "def factorial(n):",
      "sampling_params": {
        "temperature": 0.3,
        "max_tokens": 256
      }
    }
  }'

echo ""
echo ""

# Example 3: With custom parameters
echo "Example 3: Custom Parameters"
echo "--------------------------------------------------"
curl -X POST "${API_URL}" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "Explain what a binary search tree is in simple terms."}
      ],
      "sampling_params": {
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 0.9,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1
      }
    }
  }'

echo ""
echo ""
echo "=================================================="
echo "✅ Examples completed!"
echo "=================================================="
