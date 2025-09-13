#!/usr/bin/env python3
"""Test script to verify the API structure works correctly."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, '.')

def test_api_structure():
    """Test that the API structure is properly set up."""
    print("Testing NextCV API Structure")
    print("=" * 40)
    
    try:
        # Test explicit module imports
        import nextcv.api as api
        import nextcv.python as py
        import nextcv
        
        print("✓ Module imports successful")
        
        # Test C++ wrapped functions
        print("\nC++ Wrapped Functions (nextcv.api):")
        try:
            hello_result = api.hello()
            print(f"✓ api.hello(): {hello_result}")
        except Exception as e:
            print(f"✗ api.hello() failed: {e}")
            return False
        
        try:
            version = api.get_version()
            print(f"✓ api.get_version(): {version}")
        except Exception as e:
            print(f"✗ api.get_version() failed: {e}")
            return False
        
        # Test pure Python functions
        print("\nPure Python Functions (nextcv.python):")
        try:
            import numpy as np
            test_image = np.array([[0, 64, 128]], dtype=np.uint8)
            is_valid = py.validate_image(test_image)
            print(f"✓ py.validate_image(): {is_valid}")
        except Exception as e:
            print(f"✗ py.validate_image() failed: {e}")
            return False
        
        try:
            resized = py.resize_image(test_image, (2, 2))
            print(f"✓ py.resize_image(): {resized.shape}")
        except Exception as e:
            print(f"✗ py.resize_image() failed: {e}")
            return False
        
        # Test convenience imports
        print("\nConvenience Imports (nextcv):")
        try:
            hello_result = nextcv.hello()
            print(f"✓ nextcv.hello(): {hello_result}")
        except Exception as e:
            print(f"✗ nextcv.hello() failed: {e}")
            return False
        
        try:
            is_valid = nextcv.validate_image(test_image)
            print(f"✓ nextcv.validate_image(): {is_valid}")
        except Exception as e:
            print(f"✗ nextcv.validate_image() failed: {e}")
            return False
        
        # Test module attributes
        print("\nModule Structure:")
        print(f"✓ nextcv.api.__all__: {api.__all__}")
        print(f"✓ nextcv.python.__all__: {py.__all__}")
        print(f"✓ nextcv.__all_cpp__: {nextcv.__all_cpp__}")
        print(f"✓ nextcv.__all_python__: {nextcv.__all_python__}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_import_clarity():
    """Test that imports make it clear what type of code is being used."""
    print("\nImport Clarity Test:")
    
    try:
        import nextcv.api as api
        import nextcv.python as py
        
        # Check that we can distinguish between C++ and Python functions
        cpp_functions = ['hello', 'invert', 'threshold', 'nms', 'get_version', 'get_build_info']
        python_functions = ['load_image', 'save_image', 'resize_image', 'normalize_image', 
                           'validate_image', 'draw_boxes', 'draw_text', 'create_visualization_grid']
        
        print("C++ wrapped functions (api.*):")
        for func in cpp_functions:
            if hasattr(api, func):
                print(f"  ✓ api.{func}")
            else:
                print(f"  ✗ api.{func} missing")
                return False
        
        print("\nPure Python functions (py.*):")
        for func in python_functions:
            if hasattr(py, func):
                print(f"  ✓ py.{func}")
            else:
                print(f"  ✗ py.{func} missing")
                return False
        
        print("\n✓ Import clarity test passed!")
        print("  - 'api.' prefix clearly indicates C++ wrapped code")
        print("  - 'py.' prefix clearly indicates pure Python code")
        
        return True
        
    except Exception as e:
        print(f"✗ Import clarity test failed: {e}")
        return False

def main():
    """Run all API structure tests."""
    structure_ok = test_api_structure()
    clarity_ok = test_import_clarity()
    
    print("\n" + "=" * 40)
    if structure_ok and clarity_ok:
        print("✓ All API structure tests passed!")
        print("\nBenefits of this structure:")
        print("• Crystal clear distinction between C++ and Python code")
        print("• 'api.' prefix = C++ wrapped (high performance)")
        print("• 'py.' prefix = Pure Python (utilities, I/O, viz)")
        print("• Convenience imports available but less clear")
        print("• Easy to understand just by looking at imports!")
    else:
        print("✗ Some tests failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())