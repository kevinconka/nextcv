#!/usr/bin/env python3
"""Example demonstrating NextCV mixed API approach.

This example shows how to use both C++ and Python implementations
in the same modules, allowing you to choose the best implementation.
"""

import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Tuple

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def create_test_data(
    n_boxes: int = 10000,
) -> Tuple["NDArray[np.uint8]", "NDArray[np.float32]", "NDArray[np.float32]"]:
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


def create_wbf_test_data(
    n_models: int = 3,
    boxes_per_model: int = 1200,
) -> Tuple[
    list["NDArray[np.float32]"],
    list["NDArray[np.float32]"],
    list["NDArray[np.int32]"],
]:
    """Create synthetic per-model detections for WBF timing."""
    rng = np.random.default_rng(123)

    boxes_list: list["NDArray[np.float32]"] = []
    scores_list: list["NDArray[np.float32]"] = []
    labels_list: list["NDArray[np.int32]"] = []

    for _ in range(n_models):
        centers = rng.uniform(0.10, 0.90, (boxes_per_model, 2))
        sizes = rng.uniform(0.04, 0.25, (boxes_per_model, 2))
        jitter = rng.normal(0.0, 0.01, (boxes_per_model, 4))

        x1 = np.clip(centers[:, 0] - (sizes[:, 0] / 2.0) + jitter[:, 0], 0.0, 1.0)
        y1 = np.clip(centers[:, 1] - (sizes[:, 1] / 2.0) + jitter[:, 1], 0.0, 1.0)
        x2 = np.clip(centers[:, 0] + (sizes[:, 0] / 2.0) + jitter[:, 2], 0.0, 1.0)
        y2 = np.clip(centers[:, 1] + (sizes[:, 1] / 2.0) + jitter[:, 3], 0.0, 1.0)

        x2 = np.maximum(x2, x1 + 1e-4)
        y2 = np.maximum(y2, y1 + 1e-4)

        boxes = np.stack([x1, y1, x2, y2], axis=1).astype(np.float32)
        scores = rng.uniform(0.05, 1.0, boxes_per_model).astype(np.float32)
        labels = rng.integers(0, 4, boxes_per_model, dtype=np.int32)

        boxes_list.append(boxes)
        scores_list.append(scores)
        labels_list.append(labels)

    return boxes_list, scores_list, labels_list


def timed_run(function: Callable[[], Any], repeats: int = 3) -> Tuple[Any, float]:
    """Run a function multiple times and return (result, best_time_seconds)."""
    best_time = float("inf")
    result: object = None
    for _ in range(repeats):
        start_time = time.perf_counter()
        result = function()
        elapsed = time.perf_counter() - start_time
        best_time = min(best_time, elapsed)
    return result, best_time


def demonstrate_core_functionality() -> None:
    """Demonstrate core functionality with C++ and Python implementations."""
    print("Core functionality:")
    from nextcv.core import hello_cpp, hello_python

    print(f"   hello_cpp(): {hello_cpp()}")  # C++ if available, Python fallback
    print(f"   hello_python(): {hello_python()}")  # Always Python
    print()


def demonstrate_image_processing(test_image: "NDArray[np.uint8]") -> None:
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
    matrix_a = rng.standard_normal((4, 3)).astype(np.float32)
    print(f"   Matrix A ({matrix_a.shape}):")
    print(f"   {matrix_a}")

    # Vector x: 3x1
    x = rng.standard_normal((3,)).astype(np.float32)
    print(f"   Vector x ({x.shape}):")
    print(f"   {x}")

    # Compute using NextCV (Eigen)
    y_nextcv = matvec(matrix_a, x)
    print("   Result y = A @ x using NextCV (Eigen):")
    print(f"     Shape: {y_nextcv.shape}, dtype: {y_nextcv.dtype}")
    print(f"     Values: {y_nextcv}")

    # Compare with NumPy
    y_np = matrix_a @ x
    print("   Result y = A @ x using NumPy:")
    print(f"     Shape: {y_np.shape}, dtype: {y_np.dtype}")
    print(f"     Values: {y_np}")

    # Verify they match
    if np.allclose(y_nextcv, y_np, rtol=1e-6, atol=1e-6):
        print("   ✓ Results match perfectly!")
    else:
        print("   ✗ Results differ!")
    print()


def demonstrate_nms_timing(
    test_boxes: "NDArray[np.float32]",
    test_scores: "NDArray[np.float32]",
) -> None:
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
    print(f"   C++ is {np_time / cpp_time:.1f}x faster than NumPy")
    print()


def demonstrate_wbf_timing(
    boxes_list: list["NDArray[np.float32]"],
    scores_list: list["NDArray[np.float32]"],
    labels_list: list["NDArray[np.int32]"],
) -> None:
    """Demonstrate WBF functionality with performance timing."""
    print("Post-processing (WBF timing comparison):")
    from nextcv.postprocessing import wbf_cpp, wbf_np

    total_boxes = sum(len(model_boxes) for model_boxes in boxes_list)
    print(
        f"   Dataset: {len(boxes_list)} models, "
        f"{len(boxes_list[0])} boxes/model ({total_boxes} total boxes)"
    )
    print()

    # Warm-up calls
    wbf_cpp(boxes_list, scores_list, labels_list, iou_thr=0.55, skip_box_thr=0.001)
    wbf_np(boxes_list, scores_list, labels_list, iou_thr=0.55, skip_box_thr=0.001)

    (boxes_cpp, scores_cpp, labels_cpp), cpp_time = timed_run(
        lambda: wbf_cpp(
            boxes_list, scores_list, labels_list, iou_thr=0.55, skip_box_thr=0.001
        )
    )
    (boxes_np, scores_np, labels_np), np_time = timed_run(
        lambda: wbf_np(
            boxes_list, scores_list, labels_list, iou_thr=0.55, skip_box_thr=0.001
        )
    )

    print(
        f"   wbf_cpp(): {len(boxes_cpp)} boxes kept in {cpp_time * 1000:.2f}ms "
        "(best of 3)"
    )
    print(
        f"   wbf_np(): {len(boxes_np)} boxes kept in {np_time * 1000:.2f}ms (best of 3)"
    )
    print()

    # Verify parity before reporting speedup.
    boxes_match = np.allclose(boxes_cpp, boxes_np, rtol=1e-5, atol=1e-6)
    scores_match = np.allclose(scores_cpp, scores_np, rtol=1e-5, atol=1e-6)
    labels_match = np.array_equal(labels_cpp, labels_np)
    print(
        "   Match check: "
        f"boxes={boxes_match}, scores={scores_match}, labels={labels_match}"
    )

    print("Performance comparison:")
    print(f"   C++ is {np_time / cpp_time:.1f}x faster than ensemble-boxes")
    print()


def main() -> None:
    """Demonstrate the mixed API approach."""
    print("=== NextCV Mixed API Example ===")
    print("This example shows the mixed C++/Python approach")
    print()

    # Create test data
    test_image, test_boxes, test_scores = create_test_data()
    wbf_boxes_list, wbf_scores_list, wbf_labels_list = create_wbf_test_data()

    # Run demonstrations
    demonstrate_core_functionality()
    demonstrate_image_processing(test_image)
    demonstrate_linear_algebra()
    demonstrate_nms_timing(test_boxes, test_scores)
    demonstrate_wbf_timing(wbf_boxes_list, wbf_scores_list, wbf_labels_list)


if __name__ == "__main__":
    main()
