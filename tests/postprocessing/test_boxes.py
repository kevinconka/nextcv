"""Test bounding box postprocessing functions."""

import numpy as np

import nextcv.postprocessing as pp


def test_nms_np():
    """Test numpy-based NMS implementation."""
    bboxes = np.array(
        [
            [10, 10, 50, 50],  # Box 0
            [15, 15, 55, 55],  # Box 1 (overlaps with 0)
            [100, 100, 150, 150],  # Box 2 (separate)
        ],
        dtype=np.float32,
    )

    scores = np.array([0.9, 0.8, 0.7], dtype=np.float32)

    result = pp.nms_np(bboxes, scores, 0.5)

    assert isinstance(result, np.ndarray)
    assert len(result) <= 3
    # Should keep at least one box
    assert len(result) > 0
    # All indices should be valid
    assert all(0 <= idx < 3 for idx in result)


def test_nms_cpp():
    """Test C++ NMS implementation."""
    bboxes = np.array(
        [[10, 10, 50, 50], [15, 15, 55, 55], [100, 100, 150, 150]], dtype=np.float32
    )

    scores = np.array([0.9, 0.8, 0.7], dtype=np.float32)

    result = pp.nms_cpp(bboxes, scores, 0.5)

    assert isinstance(result, list)
    assert len(result) <= 3
    # Should keep at least one box
    assert len(result) > 0
    # All indices should be valid
    assert all(0 <= idx < 3 for idx in result)
