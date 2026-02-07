"""
Example usage of vLLM-pod with Python requests
"""
import requests
import os
import json

# Configuration
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY", "your-api-key-here")
ENDPOINT_ID = os.getenv("ENDPOINT_ID", "your-endpoint-id")

# Construct API URL
url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"

# Example 1: Simple code generation
def example_code_generation():
    print("=" * 60)
    print("Example 1: Simple Code Generation")
    print("=" * 60)
    
    payload = {
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Python programmer. Write clean, efficient code."
                },
                {
                    "role": "user",
                    "content": "Write a Python function to calculate the nth Fibonacci number using dynamic programming."
                }
            ],
            "sampling_params": {
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 0.9
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if response.status_code == 200:
        print("\n✅ Success!")
        if "output" in result and result["output"]:
            for output in result["output"]:
                print(f"\nGenerated code:\n{output['text']}")
                print(f"\nTokens: {output.get('tokens', 'N/A')}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"\n❌ Error: {result}")


# Example 2: Code review
def example_code_review():
    print("\n" + "=" * 60)
    print("Example 2: Code Review")
    print("=" * 60)
    
    code_to_review = """
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result
"""
    
    payload = {
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a code reviewer. Analyze the code and suggest improvements."
                },
                {
                    "role": "user",
                    "content": f"Review this Python code and suggest improvements:\n\n{code_to_review}"
                }
            ],
            "sampling_params": {
                "temperature": 0.3,
                "max_tokens": 1024
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if response.status_code == 200:
        print("\n✅ Success!")
        if "output" in result and result["output"]:
            for output in result["output"]:
                print(f"\nReview:\n{output['text']}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"\n❌ Error: {result}")


# Example 3: Using direct prompt
def example_direct_prompt():
    print("\n" + "=" * 60)
    print("Example 3: Direct Prompt")
    print("=" * 60)
    
    payload = {
        "input": {
            "prompt": "Write a Python function to check if a number is prime:",
            "sampling_params": {
                "temperature": 0.5,
                "max_tokens": 512
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if response.status_code == 200:
        print("\n✅ Success!")
        if "output" in result and result["output"]:
            for output in result["output"]:
                print(f"\nGenerated:\n{output['text']}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"\n❌ Error: {result}")


if __name__ == "__main__":
    print("vLLM-pod Python Examples")
    print()
    
    if RUNPOD_API_KEY == "your-api-key-here" or ENDPOINT_ID == "your-endpoint-id":
        print("⚠️  Please set RUNPOD_API_KEY and ENDPOINT_ID environment variables")
        print()
        print("Example:")
        print("  export RUNPOD_API_KEY='your-actual-key'")
        print("  export ENDPOINT_ID='your-endpoint-id'")
        print("  python example_usage.py")
        exit(1)
    
    try:
        example_code_generation()
        example_code_review()
        example_direct_prompt()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
