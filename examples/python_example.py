#!/usr/bin/env python3
"""Example demonstrating NextCV mixed API approach.

This example shows how to use both C++ and Python implementations
in the same modules, allowing you to choose the best implementation.
"""

import time

import numpy as np


def create_test_data(n_boxes: int = 10000) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create test data for the examples.

    Args:
        n_boxes: Number of bounding boxes to generate for NMS testing

    Returns:
        Tuple of (test_image, test_boxes, test_scores)
    """
    # Create test image
    test_image = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)

    # Create bounding boxes dataset
    rng = np.random.default_rng(42)
    test_boxes = rng.uniform(0, 100, (n_boxes, 4)).astype(np.float32)
    # Ensure boxes are valid (x1 < x2, y1 < y2)
    test_boxes[:, 2] = test_boxes[:, 0] + rng.uniform(10, 50, n_boxes)
    test_boxes[:, 3] = test_boxes[:, 1] + rng.uniform(10, 50, n_boxes)
    test_scores = rng.uniform(0.1, 1.0, n_boxes).astype(np.float32)

    return test_image, test_boxes, test_scores


def demonstrate_core_functionality() -> None:
    """Demonstrate core functionality with C++ and Python implementations."""
    print("Core functionality:")
    from nextcv.core import hello_cpp, hello_python

    print(f"   hello_cpp(): {hello_cpp()}")  # C++ if available, Python fallback
    print(f"   hello_python(): {hello_python()}")  # Always Python
    print()


def demonstrate_image_processing(test_image: np.ndarray) -> None:
    """Demonstrate image processing functionality."""
    print("Image processing:")
    from nextcv.image import invert

    print(f"   invert(): {invert(test_image)}")
    print()


def demonstrate_linear_algebra() -> None:
    """Demonstrate linear algebra functionality with Eigen."""
    print("Linear algebra (Eigen matrix-vector multiplication):")
    from nextcv.linalg import matvec

    # Create test data
    rng = np.random.default_rng(42)

    # Matrix A: 4x3
    A = rng.standard_normal((4, 3)).astype(np.float32)
    print(f"   Matrix A ({A.shape}):")
    print(f"   {A}")

    # Vector x: 3x1
    x = rng.standard_normal((3,)).astype(np.float32)
    print(f"   Vector x ({x.shape}):")
    print(f"   {x}")

    # Compute using NextCV (Eigen)
    y_nextcv = matvec(A, x)
    print("   Result y = A @ x using NextCV (Eigen):")
    print(f"     Shape: {y_nextcv.shape}, dtype: {y_nextcv.dtype}")
    print(f"     Values: {y_nextcv}")

    # Compare with NumPy
    y_np = A @ x
    print("   Result y = A @ x using NumPy:")
    print(f"     Shape: {y_np.shape}, dtype: {y_np.dtype}")
    print(f"     Values: {y_np}")

    # Verify they match
    if np.allclose(y_nextcv, y_np, rtol=1e-6, atol=1e-6):
        print("   ✓ Results match perfectly!")
    else:
        print("   ✗ Results differ!")
    print()


def demonstrate_nms_timing(test_boxes: np.ndarray, test_scores: np.ndarray) -> None:
    """Demonstrate NMS functionality with performance timing."""
    print("Post-processing (NMS timing comparison):")
    from nextcv.postprocessing import nms_cpp, nms_np

    print(f"   Dataset: {len(test_boxes)} bounding boxes")
    print()

    # Time C++ implementation
    start_time = time.perf_counter()
    result_cpp = nms_cpp(test_boxes, test_scores, 0.5)
    cpp_time = time.perf_counter() - start_time
    print(f"   nms_cpp(): {len(result_cpp)} boxes kept in {cpp_time * 1000:.2f}ms")

    # Time NumPy implementation
    start_time = time.perf_counter()
    result_np = nms_np(test_boxes, test_scores, 0.5)
    np_time = time.perf_counter() - start_time
    print(f"   nms_np(): {len(result_np)} boxes kept in {np_time * 1000:.2f}ms")

    # Performance comparison
    print()
    print("Performance comparison:")
    fastest_time = min(cpp_time, np_time)
    print(f"   Fastest: {fastest_time * 1000:.2f}ms")
    print(f"   C++ speedup: {cpp_time / fastest_time:.1f}x")
    print(f"   NumPy speedup: {np_time / fastest_time:.1f}x")
    print()


def main() -> None:
    """Demonstrate the mixed API approach."""
    print("=== NextCV Mixed API Example ===")
    print("This example shows the mixed C++/Python approach")
    print()

    # Create test data
    test_image, test_boxes, test_scores = create_test_data()

    # Run demonstrations
    demonstrate_core_functionality()
    demonstrate_image_processing(test_image)
    demonstrate_linear_algebra()
    demonstrate_nms_timing(test_boxes, test_scores)


if __name__ == "__main__":
    main()
