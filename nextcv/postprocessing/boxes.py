"""Bounding box postprocessing functions."""

from typing import TYPE_CHECKING

import numpy as np

from nextcv._cpp.nextcv_py.postprocessing import nms as _nms
from nextcv._cpp.nextcv_py.postprocessing import (
    weighted_boxes_fusion as _weighted_boxes_fusion,
)

if TYPE_CHECKING:
    from numpy.typing import NDArray


def nms_cpp(
    bboxes: "NDArray",
    scores: "NDArray",
    iou_thresh: float,
) -> "NDArray[np.int32]":
    """Non-Maximum-Supression (NMS) algorithm to remove overlapping bounding boxes.

    Args:
        bboxes: The bounding boxes as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        scores: The confidence scores for each bounding box.
        iou_thresh: The threshold for intersection over union.
    """
    return _nms(bboxes, scores, iou_thresh)


def weighted_boxes_fusion_cpp(  # noqa: PLR0913, PLR0917
    boxes_list: list["NDArray"],
    scores_list: list["NDArray"],
    labels_list: list["NDArray"],
    weights: "list[float] | None" = None,
    iou_thr: float = 0.55,
    skip_box_thr: float = 0.0,
    conf_type: str = "avg",
    allows_overflow: bool = False,
) -> tuple["NDArray[np.float32]", "NDArray[np.float32]", "NDArray[np.int32]"]:
    """Fuse detections from multiple models using Weighted Box Fusion (WBF).

    Args:
        boxes_list: Per-model boxes with shape (N_i, 4) in normalized xyxy format.
        scores_list: Per-model confidence scores with shape (N_i,).
        labels_list: Per-model integer labels with shape (N_i,).
        weights: Optional per-model weights. Defaults to equal weights.
        iou_thr: IoU threshold for clustering boxes into the same fused box.
        skip_box_thr: Drop boxes with score lower than this threshold.
        conf_type: Confidence mode. One of:
            "avg", "max", "box_and_model_avg", "absent_model_aware_avg".
        allows_overflow: If True, confidence can exceed 1.0 for avg mode.

    Returns:
        Tuple of (fused_boxes, fused_scores, fused_labels).
    """
    if weights is None:
        weights = []
    boxes, scores, labels = _weighted_boxes_fusion(
        boxes_list,
        scores_list,
        labels_list,
        weights,
        iou_thr,
        skip_box_thr,
        conf_type,
        allows_overflow,
    )
    boxes_arr = np.asarray(boxes, dtype=np.float32)
    if boxes_arr.size == 0:
        boxes_arr = boxes_arr.reshape(0, 4)
    return (
        boxes_arr,
        np.asarray(scores, dtype=np.float32),
        np.asarray(labels, dtype=np.int32),
    )


def iou_np(
    target_box: "NDArray",
    boxes: "NDArray",
    target_area: "NDArray",
    areas: "NDArray",
    inclusive: bool = False,
) -> "NDArray":
    """Calculate intersection over union of target box with all others.

    Args:
        target_box: The bounding box as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        boxes: The bounding boxes as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        target_area: The area of the target box.
        areas: The areas of all boxes.
        inclusive: If True, uses (x2 - x1 + 1) * (y2 - y1 + 1) for area.
            Enable only for integer, pixel-indexed boxes (VOC/OpenCV style).

    Returns:
        The intersection over union of the target box with all others.
    """
    # Intersection corners via broadcasting
    tl = np.maximum(boxes[:, :2], target_box[:2])  # (N,2)
    br = np.minimum(boxes[:, 2:], target_box[2:])  # (N,2)

    # Calculate intersection area
    add = 1.0 if inclusive else 0.0
    wh = np.clip(br - tl + add, 0.0, None)  # (N,2)
    inter = wh[:, 0] * wh[:, 1]  # (N,)

    union = target_area + areas - inter
    return inter / np.clip(union, 1e-7, None)


def nms_np(
    bboxes: "NDArray",
    scores: "NDArray",
    iou_thresh: float,
) -> "NDArray":
    """Non-Maximum-Supression (NMS) algorithm to remove overlapping bounding boxes.

    Args:
        bboxes: The bounding boxes as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        scores: The confidence scores for each bounding box.
        iou_thresh: The threshold for intersection over union.

    Returns:
        The indices of the bounding boxes to keep.
    """
    bboxes = bboxes.astype(np.float32)
    x1, y1 = bboxes[..., 0], bboxes[..., 1]  # top left
    x2, y2 = bboxes[..., 2], bboxes[..., 3]  # bottom right

    areas = (x2 - x1) * (y2 - y1)  # calculate area per bbox
    order = np.argsort(scores)[::-1]  # sort by descending confidence

    keep = np.zeros_like(scores, dtype=bool)  # which boxes (idx) to keep

    while order.size > 0:
        # take current highest confidence box
        i = order[0]
        keep[i] = True

        # If this is the last box, we're done
        if order.size == 1:
            break

        # calculate intersection over union with all other boxes
        ovr = iou_np(bboxes[i], bboxes[order[1:]], areas[i], areas[order[1:]])

        # find boxes to keep since they are not overlapping enough
        idxs = np.nonzero(ovr <= iou_thresh)[0]

        # update order by removing suppressed boxes
        order = order[idxs + 1]  # +1 because we removed the first element

    keep_indices = np.nonzero(keep)[0]
    return keep_indices[np.argsort(scores[keep_indices])[::-1]]
