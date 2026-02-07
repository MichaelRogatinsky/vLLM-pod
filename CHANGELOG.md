# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-07

### Added
- Initial implementation of vLLM-pod for Qwen3-Coder-Next
- Dockerfile with CUDA 12.1.1 and Python 3.11
- vLLM engine wrapper with proper tokenizer configuration
- RunPod serverless handler
- Latest dependency versions (vLLM 0.7.1+, Transformers 4.46.0+)
- Comprehensive README with usage instructions
- Deployment guide documentation
- Example scripts (Python and cURL)
- Build script for easy Docker image creation
- docker-compose.yml for local testing
- Basic test suite
- MIT License
- .gitignore for build artifacts

### Fixed
- Tokenizer issues with Qwen3-Coder-Next by:
  - Setting `TOKENIZER_MODE=auto` for automatic tokenizer handling
  - Enabling `TRUST_REMOTE_CODE=true` for Qwen models
  - Using latest transformers library (4.46.0+) with proper Qwen3 support
  - Proper tokenizer initialization using vLLM's `get_tokenizer()`

### Configuration
- Support for up to 256K context length (configurable via `MAX_MODEL_LEN`)
- Configurable GPU memory utilization
- Support for tensor parallelism across multiple GPUs
- Optional quantization support (AWQ, GPTQ, etc.)
- Automatic chat template application

### Documentation
- Complete deployment guide for RunPod Serverless
- Troubleshooting section for common issues
- Hardware requirements and recommendations
- Cost optimization tips
- Example usage scripts

## Features

### Core Functionality
- OpenAI-compatible API interface
- Support for both message-based and direct prompt inputs
- Streaming and non-streaming response modes
- Configurable sampling parameters
- Automatic model downloading from Hugging Face

### Optimizations
- Flash Attention 2 support
- Efficient GPU memory utilization
- Tensor parallelism for multi-GPU setups
- Configurable batch sizes for throughput optimization

### Developer Experience
- Simple build script for image creation
- Local testing with docker-compose
- Comprehensive examples and documentation
- Clear error messages and logging
