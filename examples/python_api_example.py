#!/usr/bin/env python3
"""Example demonstrating NextCV API structure - C++ vs Pure Python.

This example shows how to distinguish between C++ wrapped functions
and pure Python functions by looking at the import pattern.
"""

import numpy as np

# Method 1: Explicit module imports (RECOMMENDED)
# This makes it crystal clear what type of code you're using
import nextcv.api as api          # C++ wrapped functions
import nextcv.python as py        # Pure Python functions

def main():
    """Demonstrate different import patterns and their clarity."""
    print("=== NextCV API Structure Example ===")
    print("This example shows how to distinguish C++ vs Pure Python code")
    print()
    
    # Create some test data
    test_image = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    test_boxes = [(10, 10, 50, 50), (100, 100, 30, 30)]
    
    print("1. C++ Wrapped Functions (High Performance)")
    print("   Import: import nextcv.api as api")
    print("   Usage:  api.function_name()")
    print()
    
    # C++ wrapped functions - clearly marked by 'api.' prefix
    print("   C++ wrapped functions:")
    print(f"   - api.hello(): {api.hello()}")
    print(f"   - api.get_version(): {api.get_version()}")
    
    # Image processing with C++ backend
    inverted = api.invert(test_image)
    print(f"   - api.invert(): {test_image} -> {inverted}")
    
    thresholded = api.threshold(test_image, 128)
    print(f"   - api.threshold(): {test_image} -> {thresholded}")
    
    # NMS with C++ backend
    print(f"   - api.nms(): Available for bounding box filtering")
    print()
    
    print("2. Pure Python Functions (Utilities & I/O)")
    print("   Import: import nextcv.python as py")
    print("   Usage:  py.function_name()")
    print()
    
    # Pure Python functions - clearly marked by 'py.' prefix
    print("   Pure Python functions:")
    print(f"   - py.validate_image(): {py.validate_image(test_image)}")
    
    # Image utilities
    resized = py.resize_image(test_image, (3, 3))
    print(f"   - py.resize_image(): Resized to {resized.shape}")
    
    normalized = py.normalize_image(test_image)
    print(f"   - py.normalize_image(): Normalized to range [{normalized.min():.2f}, {normalized.max():.2f}]")
    
    # Visualization
    print(f"   - py.draw_boxes(): Available for drawing bounding boxes")
    print(f"   - py.draw_text(): Available for drawing text")
    print(f"   - py.load_image(): Available for loading images from files")
    print(f"   - py.save_image(): Available for saving images to files")
    print()
    
    print("3. Convenience Imports (Mixed)")
    print("   Import: import nextcv")
    print("   Usage:  nextcv.function_name()")
    print("   Note:   Less clear which functions are C++ vs Python")
    print()
    
    # Convenience imports - less clear about implementation
    import nextcv
    print("   Convenience imports (mixed C++ and Python):")
    print(f"   - nextcv.hello(): {nextcv.hello()}  # C++ wrapped")
    print(f"   - nextcv.invert(): {nextcv.invert(test_image)}  # C++ wrapped")
    print(f"   - nextcv.validate_image(): {nextcv.validate_image(test_image)}  # Pure Python")
    print()
    
    print("4. Import Pattern Summary")
    print("   " + "="*50)
    print("   | Import Pattern    | Code Type    | Performance | Clarity |")
    print("   " + "="*50)
    print("   | nextcv.api.*      | C++ wrapped  | High       | High    |")
    print("   | nextcv.python.*   | Pure Python  | Medium     | High    |")
    print("   | nextcv.*          | Mixed        | Mixed      | Low     |")
    print("   " + "="*50)
    print()
    
    print("5. Recommendations")
    print("   - Use 'nextcv.api' for performance-critical operations")
    print("   - Use 'nextcv.python' for utilities, I/O, and visualization")
    print("   - Use 'nextcv' convenience imports only for simple scripts")
    print("   - The 'api' and 'python' prefixes make it immediately clear")
    print("     what type of code you're working with!")


if __name__ == "__main__":
    main()