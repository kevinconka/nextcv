#!/usr/bin/env python3
"""Simplified NextCV example demonstrating the essential functionality.

This example shows the simplified structure with only essential functions:
- cvx.image.invert() - C++ wrapped
- cvx.postprocessing.nms_fast() - C++ wrapped  
- cvx.postprocessing.nms() - Native Python
- cvx.core.hello() - C++ wrapped
"""

import nextcv as cvx
import numpy as np

def main():
    """Demonstrate the simplified NextCV API."""
    print("=== NextCV Simplified Example ===")
    print("Essential functions only - clean and simple!")
    print()
    
    # Create test data
    test_image = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    test_boxes = [(10, 10, 50, 50, 0.9), (15, 15, 45, 45, 0.8), (100, 100, 30, 30, 0.7)]
    
    print("1. Core functionality:")
    print(f"   cvx.core.hello(): {cvx.core.hello()}")
    print()
    
    print("2. Image processing:")
    print(f"   cvx.image.invert(): {cvx.image.invert(test_image)}")
    print(f"   cvx.image.invert_python(): {cvx.image.invert_python(test_image)}")
    print()
    
    print("3. Post-processing:")
    print(f"   cvx.postprocessing.nms(): {len(cvx.postprocessing.nms(test_boxes, 0.5))} boxes")
    print(f"   cvx.postprocessing.nms_fast(): {len(cvx.postprocessing.nms_fast(test_boxes, 0.5))} boxes")
    print()
    
    print("4. Import pattern:")
    print("   import nextcv as cvx")
    print("   cvx.image.invert(image)        # C++ wrapped")
    print("   cvx.postprocessing.nms_fast()  # C++ wrapped")
    print("   cvx.postprocessing.nms()       # Native Python")
    print("   cvx.core.hello()               # C++ wrapped")
    print()
    
    print("5. Benefits of simplified structure:")
    print("   ✓ Only essential functions")
    print("   ✓ Clear module.function() syntax")
    print("   ✓ C++ for performance, Python for debugging")
    print("   ✓ Easy to understand and extend")
    print("   ✓ Clean PR with minimal changes")


if __name__ == "__main__":
    main()