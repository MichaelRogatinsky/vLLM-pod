"""
vLLM Engine wrapper for Qwen3-Coder-Next
Handles initialization and inference with proper tokenizer configuration
"""
import os
from vllm import LLM, SamplingParams
from vllm.transformers_utils.tokenizer import get_tokenizer
import logging

logger = logging.getLogger(__name__)


class VLLMEngine:
    """vLLM Engine wrapper with Qwen3-Coder-Next optimizations"""
    
    def __init__(self):
        """Initialize the vLLM engine with environment configuration"""
        # Get configuration from environment
        self.model_name = os.getenv("MODEL_NAME", "Qwen/Qwen3-Coder-Next")
        self.max_model_len = int(os.getenv("MAX_MODEL_LEN", "32768"))
        self.gpu_memory_utilization = float(os.getenv("GPU_MEMORY_UTILIZATION", "0.90"))
        self.tensor_parallel_size = int(os.getenv("TENSOR_PARALLEL_SIZE", "1"))
        self.trust_remote_code = os.getenv("TRUST_REMOTE_CODE", "true").lower() == "true"
        self.quantization = os.getenv("QUANTIZATION", None)
        self.max_num_seqs = int(os.getenv("MAX_NUM_SEQS", "256"))
        self.tokenizer_mode = os.getenv("TOKENIZER_MODE", "auto")
        
        logger.info(f"Initializing vLLM with model: {self.model_name}")
        logger.info(f"Configuration: max_len={self.max_model_len}, "
                   f"gpu_util={self.gpu_memory_utilization}, "
                   f"tensor_parallel={self.tensor_parallel_size}, "
                   f"tokenizer_mode={self.tokenizer_mode}")
        
        # Initialize the LLM
        self.llm = LLM(
            model=self.model_name,
            max_model_len=self.max_model_len,
            gpu_memory_utilization=self.gpu_memory_utilization,
            tensor_parallel_size=self.tensor_parallel_size,
            trust_remote_code=self.trust_remote_code,
            quantization=self.quantization if self.quantization else None,
            max_num_seqs=self.max_num_seqs,
            tokenizer_mode=self.tokenizer_mode,
        )
        
        # Get tokenizer for chat template
        self.tokenizer = get_tokenizer(
            self.model_name,
            trust_remote_code=self.trust_remote_code,
            tokenizer_mode=self.tokenizer_mode
        )
        
        logger.info("vLLM engine initialized successfully")
    
    def generate(self, params):
        """
        Generate text based on input parameters
        
        Args:
            params: Dictionary containing generation parameters
            
        Returns:
            Dictionary with generated text or error
        """
        try:
            # Extract parameters
            messages = params.get("messages")
            prompt = params.get("prompt")
            sampling_params_dict = params.get("sampling_params", {})
            stream = params.get("stream", False)
            
            # Apply chat template if messages are provided
            if messages:
                if hasattr(self.tokenizer, 'apply_chat_template'):
                    prompt = self.tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                else:
                    # Fallback for tokenizers without chat template
                    prompt = self._format_messages(messages)
                    
            if not prompt:
                return {"error": "No prompt or messages provided"}
            
            # Set up sampling parameters
            sampling_params = SamplingParams(
                temperature=sampling_params_dict.get("temperature", 0.7),
                top_p=sampling_params_dict.get("top_p", 0.9),
                max_tokens=sampling_params_dict.get("max_tokens", 2048),
                n=sampling_params_dict.get("n", 1),
                stop=sampling_params_dict.get("stop", None),
                presence_penalty=sampling_params_dict.get("presence_penalty", 0.0),
                frequency_penalty=sampling_params_dict.get("frequency_penalty", 0.0),
            )
            
            logger.info(f"Generating with prompt length: {len(prompt)}")
            
            # Generate
            outputs = self.llm.generate([prompt], sampling_params)
            
            # Format output
            result = {
                "output": [],
                "model": self.model_name,
            }
            
            for output in outputs:
                for completion in output.outputs:
                    result["output"].append({
                        "text": completion.text,
                        "finish_reason": completion.finish_reason,
                        "tokens": len(completion.token_ids),
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}", exc_info=True)
            return {"error": str(e)}
    
    def _format_messages(self, messages):
        """
        Fallback message formatter for tokenizers without chat template
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Formatted prompt string
        """
        formatted = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"
        
        formatted += "Assistant: "
        return formatted
