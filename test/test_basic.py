"""
Test script for vLLM engine
Tests basic functionality without GPU requirements
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import runpod
        print("✓ runpod imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import runpod: {e}")
        return False
    
    try:
        from vllm import LLM, SamplingParams
        print("✓ vllm imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import vllm: {e}")
        return False
    
    try:
        import transformers
        print(f"✓ transformers imported successfully (version: {transformers.__version__})")
    except ImportError as e:
        print(f"✗ Failed to import transformers: {e}")
        return False
    
    try:
        import torch
        print(f"✓ torch imported successfully (version: {torch.__version__})")
    except ImportError as e:
        print(f"✗ Failed to import torch: {e}")
        return False
    
    return True

def test_handler_module():
    """Test that handler module can be imported"""
    print("\nTesting handler module...")
    try:
        import handler
        print("✓ handler module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import handler: {e}")
        return False

def test_engine_module():
    """Test that engine module can be imported"""
    print("\nTesting engine module...")
    try:
        import vllm_engine
        print("✓ vllm_engine module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import vllm_engine: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("vLLM-pod Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Handler Module", test_handler_module()))
    results.append(("Engine Module", test_engine_module()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
