#!/usr/bin/env python3
"""Example demonstrating NextCV mixed API approach.

This example shows how to use both C++ and Python implementations
in the same modules, allowing you to choose the best implementation.
"""

import numpy as np

def main():
    """Demonstrate the mixed API approach."""
    print("=== NextCV Mixed API Example ===")
    print("This example shows the mixed C++/Python approach")
    print()
    
    # Create some test data
    test_image = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    test_boxes = [(10, 10, 50, 50, 0.9), (15, 15, 45, 45, 0.8), (100, 100, 30, 30, 0.7)]
    
    print("1. Mixed Modules - C++ as default, Python as fallback")
    print("   " + "="*60)
    print()
    
    # Core functionality
    print("Core functionality:")
    from nextcv.core import hello, get_version, hello_python, get_version_python
    
    print(f"   hello(): {hello()}")  # C++ if available, Python fallback
    print(f"   hello_python(): {hello_python()}")  # Always Python
    print(f"   get_version(): {get_version()}")
    print(f"   get_version_python(): {get_version_python()}")
    print()
    
    # Image processing
    print("Image processing:")
    from nextcv.image import invert, threshold, invert_python, threshold_python
    
    print(f"   invert(): {invert(test_image)}")  # C++ if available, Python fallback
    print(f"   invert_python(): {invert_python(test_image)}")  # Always Python
    print(f"   threshold(): {threshold(test_image, 128)}")
    print(f"   threshold_python(): {threshold_python(test_image, 128)}")
    print()
    
    # Post-processing
    print("Post-processing:")
    from nextcv.postprocessing import nms, fast_nms, nms_python
    
    print(f"   nms(): {len(nms(test_boxes, 0.5))} boxes")  # C++ if available, Python fallback
    print(f"   fast_nms(): {len(fast_nms(test_boxes, 0.5))} boxes")  # Alias for C++
    print(f"   nms_python(): {len(nms_python(test_boxes, 0.5))} boxes")  # Always Python
    print()
    
    # Utilities (Python-only)
    print("Utilities (Python-only):")
    from nextcv.utils import load_image, save_image, resize_image, draw_boxes
    
    print(f"   validate_image(): {validate_image(test_image)}")
    resized = resize_image(test_image, (3, 3))
    print(f"   resize_image(): {resized.shape}")
    
    # Draw boxes
    image_with_boxes = draw_boxes(test_image, [(0, 0, 2, 1)])
    print(f"   draw_boxes(): {image_with_boxes.shape}")
    print()
    
    # Features (Python-only for now)
    print("Features (Python-only for now):")
    from nextcv.features import detect_corners, detect_corners_python
    
    # Create a simple test image
    test_img = np.array([[0, 0, 0], [0, 255, 0], [0, 0, 0]], dtype=np.uint8)
    corners = detect_corners(test_img)
    print(f"   detect_corners(): {len(corners)} corners found")
    print(f"   detect_corners_python(): {len(detect_corners_python(test_img))} corners found")
    print()
    
    print("2. Import Patterns")
    print("   " + "="*60)
    print()
    
    print("Functional modules with mixed implementations:")
    print("   from nextcv.image import invert, invert_python")
    print("   from nextcv.postprocessing import nms, fast_nms, nms_python")
    print("   from nextcv.core import hello, hello_python")
    print()
    
    print("Utility modules (Python-only):")
    print("   from nextcv.utils import load_image, save_image, draw_boxes")
    print("   from nextcv.features import detect_corners")
    print()
    
    print("3. Benefits of Mixed Approach")
    print("   " + "="*60)
    print()
    print("✓ Intuitive: Functions are grouped by functionality")
    print("✓ Flexible: Choose C++ for performance, Python for debugging")
    print("✓ Clear: Implementation type is obvious from function name")
    print("✓ Extensible: Easy to add new implementations")
    print("✓ Fallback: Python implementations work when C++ isn't available")
    print()
    
    print("4. Naming Convention")
    print("   " + "="*60)
    print()
    print("• function_name() - Default implementation (C++ if available, Python fallback)")
    print("• function_name_python() - Always Python implementation")
    print("• fast_function_name() - Alias for C++ implementation")
    print("• function_name_cpp() - Explicit C++ implementation (future)")
    print()
    
    print("5. Usage Examples")
    print("   " + "="*60)
    print()
    print("# Performance-critical code")
    print("result = nextcv.invert(image)  # Uses C++ if available")
    print()
    print("# Debugging or when C++ not available")
    print("result = nextcv.invert_python(image)  # Always Python")
    print()
    print("# Explicit C++ usage")
    print("result = nextcv.fast_nms(boxes, 0.5)  # C++ implementation")
    print()
    print("# Utilities (always Python)")
    print("image = nextcv.load_image('input.jpg')")
    print("nextcv.draw_boxes(image, boxes)")


if __name__ == "__main__":
    main()