"""Test bounding box postprocessing functions."""

import numpy as np
import pytest

import nextcv.postprocessing as pp

# Test cases for NMS implementations
NMS_TEST_CASES = [
    pytest.param(
        "2 non-overlapping boxes",
        np.array([[10, 10, 50, 50], [100, 100, 150, 150]], dtype=np.float32),
        np.array([0.9, 0.8], dtype=np.float32),
        0.5,
        id="non_overlapping",
    ),
    pytest.param(
        "2 overlapping boxes",
        np.array([[10, 10, 50, 50], [15, 15, 55, 55]], dtype=np.float32),
        np.array([0.9, 0.8], dtype=np.float32),
        0.5,
        id="overlapping",
    ),
    pytest.param(
        "3 boxes with overlap",
        np.array(
            [[10, 10, 50, 50], [15, 15, 55, 55], [100, 100, 150, 150]],
            dtype=np.float32,
        ),
        np.array([0.9, 0.8, 0.7], dtype=np.float32),
        0.5,
        id="three_boxes",
    ),
    pytest.param(
        "1 box only",
        np.array([[10, 10, 50, 50]], dtype=np.float32),
        np.array([0.9], dtype=np.float32),
        0.5,
        id="single_box",
    ),
    pytest.param(
        "Empty input",
        np.array([], dtype=np.float32).reshape(0, 4),
        np.array([], dtype=np.float32),
        0.5,
        id="empty_input",
    ),
    pytest.param(
        "High overlap threshold",
        np.array(
            [[10, 10, 50, 50], [15, 15, 55, 55], [100, 100, 150, 150]],
            dtype=np.float32,
        ),
        np.array([0.9, 0.8, 0.7], dtype=np.float32),
        0.9,  # Very high threshold - should keep more boxes
        id="high_threshold",
    ),
    pytest.param(
        "Low overlap threshold",
        np.array(
            [[10, 10, 50, 50], [15, 15, 55, 55], [100, 100, 150, 150]],
            dtype=np.float32,
        ),
        np.array([0.9, 0.8, 0.7], dtype=np.float32),
        0.1,  # Very low threshold - should keep fewer boxes
        id="low_threshold",
    ),
    pytest.param(
        "Nearly identical scores",
        np.array(
            [[10, 10, 50, 50], [15, 15, 55, 55], [100, 100, 150, 150]],
            dtype=np.float32,
        ),
        np.array(
            [0.9, 0.9001, 0.9], dtype=np.float32
        ),  # Slightly different to avoid tie-breaking
        0.5,
        id="identical_scores",
    ),
]


@pytest.mark.parametrize("description,bboxes,scores,threshold", NMS_TEST_CASES)
def test_nms_implementations_match(
    description: str, bboxes: np.ndarray, scores: np.ndarray, threshold: float
):
    """Test that C++ and NumPy NMS implementations produce identical results."""
    result_cpp = pp.nms_cpp(bboxes, scores, threshold)
    result_np = pp.nms_np(bboxes, scores, threshold)

    # Both should return numpy arrays
    assert isinstance(result_cpp, np.ndarray), (
        f"C++ result should be numpy array for {description}"
    )
    assert isinstance(result_np, np.ndarray), (
        f"NumPy result should be numpy array for {description}"
    )

    # Results should be identical
    assert np.array_equal(result_cpp, result_np), (
        f"Results don't match for {description}: C++={result_cpp}, NumPy={result_np}"
    )

    # Results should be sorted (NMS typically returns indices in score order)
    if len(result_cpp) > 1:
        # Check that indices are in descending score order
        result_scores = scores[result_cpp]
        assert np.all(result_scores[:-1] >= result_scores[1:]), (
            f"Results not in score order for {description}"
        )

    # All indices should be valid
    if len(bboxes) > 0:
        assert all(0 <= idx < len(bboxes) for idx in result_cpp), (
            f"Invalid indices in C++ result for {description}"
        )
        assert all(0 <= idx < len(bboxes) for idx in result_np), (
            f"Invalid indices in NumPy result for {description}"
        )


@pytest.mark.parametrize(
    "n_boxes,threshold", [(100, 0.5), (1000, 0.5), (100, 0.1), (100, 0.9)]
)
def test_nms_large_dataset(n_boxes: int, threshold: float):
    """Test NMS implementations with larger datasets to ensure they scale correctly."""
    # Create a test dataset using modern NumPy random generator
    rng = np.random.default_rng(42)
    bboxes = rng.uniform(0, 100, (n_boxes, 4)).astype(np.float32)
    # Ensure boxes are valid (x1 < x2, y1 < y2)
    bboxes[:, 2] = bboxes[:, 0] + rng.uniform(10, 50, n_boxes)
    bboxes[:, 3] = bboxes[:, 1] + rng.uniform(10, 50, n_boxes)
    scores = rng.uniform(0.1, 1.0, n_boxes).astype(np.float32)

    result_cpp = pp.nms_cpp(bboxes, scores, threshold)
    result_np = pp.nms_np(bboxes, scores, threshold)

    # Results should be identical
    assert np.array_equal(result_cpp, result_np), "Large dataset results don't match"

    # Results should be reasonable (at least one box, not more than total)
    assert 0 < len(result_cpp) <= n_boxes, "Result count seems unreasonable"
    assert 0 < len(result_np) <= n_boxes, "Result count seems unreasonable"
