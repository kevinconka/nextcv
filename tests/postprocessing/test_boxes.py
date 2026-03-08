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


def test_weighted_boxes_fusion_cpp_basic_fusion():
    """Test deterministic WBF fusion result against expected values."""
    boxes_list = [
        np.array([[0.10, 0.10, 0.40, 0.40]], dtype=np.float32),
        np.array([[0.12, 0.12, 0.42, 0.42]], dtype=np.float32),
    ]
    scores_list = [
        np.array([0.90], dtype=np.float32),
        np.array([0.80], dtype=np.float32),
    ]
    labels_list = [
        np.array([1], dtype=np.int32),
        np.array([1], dtype=np.int32),
    ]

    boxes, scores, labels = pp.weighted_boxes_fusion_cpp(
        boxes_list,
        scores_list,
        labels_list,
        weights=[2.0, 1.0],
        iou_thr=0.5,
        skip_box_thr=0.0,
        conf_type="avg",
        allows_overflow=False,
    )

    assert boxes.shape == (1, 4)
    assert scores.shape == (1,)
    assert labels.shape == (1,)
    np.testing.assert_array_equal(labels, np.array([1], dtype=np.int32))
    np.testing.assert_allclose(
        boxes[0],
        np.array([0.10615385, 0.10615385, 0.40615386, 0.40615386], dtype=np.float32),
        rtol=1e-5,
        atol=1e-6,
    )
    np.testing.assert_allclose(
        scores, np.array([0.8666667], dtype=np.float32), rtol=1e-5, atol=1e-6
    )


def test_weighted_boxes_fusion_cpp_skip_threshold():
    """Test that skip_box_thr removes low-confidence boxes."""
    boxes_list = [
        np.array([[0.10, 0.10, 0.40, 0.40]], dtype=np.float32),
        np.array([[0.11, 0.11, 0.41, 0.41]], dtype=np.float32),
    ]
    scores_list = [
        np.array([0.20], dtype=np.float32),
        np.array([0.25], dtype=np.float32),
    ]
    labels_list = [
        np.array([0], dtype=np.int32),
        np.array([0], dtype=np.int32),
    ]

    boxes, scores, labels = pp.weighted_boxes_fusion_cpp(
        boxes_list, scores_list, labels_list, skip_box_thr=0.3
    )

    assert boxes.shape == (0, 4)
    assert scores.shape == (0,)
    assert labels.shape == (0,)


def test_weighted_boxes_fusion_cpp_conf_type_max():
    """Test `max` confidence mode matches reference confidence scaling."""
    boxes_list = [
        np.array([[0.20, 0.20, 0.50, 0.50]], dtype=np.float32),
        np.array([[0.20, 0.20, 0.50, 0.50]], dtype=np.float32),
    ]
    scores_list = [
        np.array([0.80], dtype=np.float32),
        np.array([0.70], dtype=np.float32),
    ]
    labels_list = [
        np.array([2], dtype=np.int32),
        np.array([2], dtype=np.int32),
    ]

    _, scores, labels = pp.weighted_boxes_fusion_cpp(
        boxes_list,
        scores_list,
        labels_list,
        weights=[2.0, 1.0],
        conf_type="max",
    )

    np.testing.assert_array_equal(labels, np.array([2], dtype=np.int32))
    np.testing.assert_allclose(
        scores, np.array([0.8], dtype=np.float32), rtol=1e-6, atol=1e-6
    )


def test_weighted_boxes_fusion_cpp_invalid_conf_type():
    """Test invalid conf_type raises ValueError."""
    boxes_list = [np.array([[0.10, 0.10, 0.40, 0.40]], dtype=np.float32)]
    scores_list = [np.array([0.90], dtype=np.float32)]
    labels_list = [np.array([1], dtype=np.int32)]

    with pytest.raises(ValueError):
        pp.weighted_boxes_fusion_cpp(
            boxes_list, scores_list, labels_list, conf_type="unsupported"
        )


def test_wbf_cpp_alias_matches_weighted_boxes_fusion_cpp():
    """Test short API alias `wbf_cpp` matches compatibility alias."""
    boxes_list = [np.array([[0.10, 0.10, 0.40, 0.40]], dtype=np.float32)]
    scores_list = [np.array([0.90], dtype=np.float32)]
    labels_list = [np.array([1], dtype=np.int32)]

    result_short = pp.wbf_cpp(boxes_list, scores_list, labels_list)
    result_long = pp.weighted_boxes_fusion_cpp(boxes_list, scores_list, labels_list)

    for out_short, out_long in zip(result_short, result_long, strict=True):
        np.testing.assert_array_equal(out_short, out_long)


def test_wbf_cpp_matches_wbf_np_reference_implementation():
    """Test C++ WBF output against `ensemble_boxes` reference output."""
    boxes_list = [
        np.array(
            [
                [0.00, 0.51, 0.81, 0.91],
                [0.10, 0.31, 0.71, 0.61],
                [0.01, 0.32, 0.83, 0.93],
                [0.02, 0.53, 0.11, 0.94],
                [0.03, 0.24, 0.12, 0.35],
            ],
            dtype=np.float32,
        ),
        np.array(
            [
                [0.04, 0.56, 0.84, 0.92],
                [0.12, 0.33, 0.72, 0.64],
                [0.38, 0.66, 0.79, 0.95],
                [0.08, 0.49, 0.21, 0.89],
            ],
            dtype=np.float32,
        ),
    ]
    scores_list = [
        np.array([0.9, 0.8, 0.2, 0.4, 0.7], dtype=np.float32),
        np.array([0.5, 0.8, 0.7, 0.3], dtype=np.float32),
    ]
    labels_list = [
        np.array([0, 1, 0, 1, 1], dtype=np.int32),
        np.array([1, 1, 1, 0], dtype=np.int32),
    ]

    boxes_cpp, scores_cpp, labels_cpp = pp.wbf_cpp(
        boxes_list,
        scores_list,
        labels_list,
        weights=[2.0, 1.0],
        iou_thr=0.5,
        skip_box_thr=0.0001,
    )
    boxes_np, scores_np, labels_np = pp.wbf_np(
        boxes_list,
        scores_list,
        labels_list,
        weights=[2.0, 1.0],
        iou_thr=0.5,
        skip_box_thr=0.0001,
    )

    assert boxes_cpp.dtype == np.float32
    assert scores_cpp.dtype == np.float32
    assert labels_cpp.dtype == np.int32
    np.testing.assert_allclose(boxes_cpp, boxes_np, rtol=1e-5, atol=1e-6)
    np.testing.assert_allclose(scores_cpp, scores_np, rtol=1e-5, atol=1e-6)
    np.testing.assert_array_equal(labels_cpp, labels_np)
