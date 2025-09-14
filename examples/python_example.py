#!/usr/bin/env python3
"""Example demonstrating NextCV mixed API approach.

This example shows how to use both C++ and Python implementations
in the same modules, allowing you to choose the best implementation.
"""

import numpy as np


def main() -> None:
    """Demonstrate the mixed API approach."""
    print("=== NextCV Mixed API Example ===")
    print("This example shows the mixed C++/Python approach")
    print()

    # Create some test data
    test_image = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    test_boxes = np.array(
        [(10, 10, 50, 50, 0.9), (15, 15, 45, 45, 0.8), (100, 100, 30, 30, 0.7)]
    )
    test_scores = np.array([0.9, 0.8, 0.7])

    # Core functionality
    print("Core functionality:")
    from nextcv.core import hello_cpp, hello_python

    print(f"   hello(): {hello_cpp()}")  # C++ if available, Python fallback
    print(f"   hello_python(): {hello_python()}")  # Always Python
    print()

    # Image processing
    print("Image processing:")
    from nextcv.image import invert

    print(f"   invert(): {invert(test_image)}")
    print()

    # Post-processing
    print("Post-processing:")
    from nextcv.postprocessing import nms_cpp, nms_cv2, nms_np

    print(f"   nms_cpp(): {len(nms_cpp(test_boxes, test_scores, 0.5))} boxes")
    print(f"   nms_cv2(): {len(nms_cv2(test_boxes, test_scores, 0.5))} boxes")
    print(f"   nms_np(): {len(nms_np(test_boxes, test_scores, 0.5))} boxes")
    print()


if __name__ == "__main__":
    main()
