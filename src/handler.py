"""
RunPod Handler for vLLM with Qwen3-Coder-Next
Handles both OpenAI-compatible and standard vLLM requests
"""
import os
import runpod
from vllm_engine import VLLMEngine
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize vLLM engine
logger.info("Initializing vLLM engine...")
engine = VLLMEngine()
logger.info("vLLM engine initialized successfully")


def handler(job):
    """
    Handler function for RunPod serverless
    
    Args:
        job: RunPod job containing input data
        
    Returns:
        Dictionary with output or error
    """
    try:
        job_input = job["input"]
        logger.info(f"Received job input: {job_input}")
        
        # Check if this is an OpenAI-compatible request
        if "messages" in job_input or "prompt" in job_input:
            # Handle text generation request
            result = engine.generate(job_input)
            return result
        else:
            return {"error": "Invalid input format. Expected 'messages' or 'prompt' in input."}
            
    except Exception as e:
        logger.error(f"Error processing job: {str(e)}", exc_info=True)
        return {"error": str(e)}


if __name__ == "__main__":
    logger.info("Starting RunPod serverless worker...")
    runpod.serverless.start({"handler": handler})
