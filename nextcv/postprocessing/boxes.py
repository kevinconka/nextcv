"""Bounding box postprocessing functions."""

from typing import TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray
else:
    # At runtime, just alias to ndarray so code still runs
    NDArray = np.ndarray


def iou_np(
    target_box: NDArray,
    boxes: NDArray,
    target_area: NDArray,
    areas: NDArray,
    inclusive: bool = False,
) -> NDArray:
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
    bboxes: NDArray,
    scores: NDArray,
    iou_thresh: float,
) -> NDArray:
    """Non-Maximum-Supression (NMS) algorithm to remove overlapping bounding boxes.

    Args:
        bboxes: The bounding boxes as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        scores: The confidence scores for each bounding box.
        iou_thresh: The threshold for intersection over union.
        classes: The class labels for each bounding box.
            if None, all boxes are treated as the same class (agnostic NMS).

    Returns:
        The indices of the bounding boxes to keep.
    """
    bboxes = bboxes.astype(np.float32)
    x1, y1 = bboxes[..., 0], bboxes[..., 1]  # top left
    x2, y2 = bboxes[..., 2], bboxes[..., 3]  # bottom right

    areas = (x2 - x1) * (y2 - y1)  # calculate area per bbox
    order = np.argsort(scores)[::-1]  # sort by descending confidence

    keep = np.zeros_like(scores, dtype=bool)  # which boxes (idx) to keep

    while order.size > 1:
        # take current highest confidence box
        i = order[0]
        keep[i] = True

        # calculate intersection over union with all other boxes
        ovr = iou_np(bboxes[i], bboxes[order[1:]], areas[i], areas[order[1:]])

        # find boxes to keep since they are not overlapping enough
        idxs = np.nonzero(ovr <= iou_thresh)[0]

        # update order by removing suppressed boxes
        order = order[idxs + 1]  # +1 because we removed the first element

    return np.nonzero(keep)[0]  # indices of boxes to keep


def nms_cv2(
    bboxes: NDArray,
    scores: NDArray,
    iou_thresh: float,
) -> NDArray:
    """Non-Maximum-Supression (NMS) using OpenCV's dnn.NMSBoxes().

    Args:
        bboxes: The bounding boxes as
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y).
        scores: The confidence scores for each bounding box.
        iou_thresh: The threshold for intersection over union.

    Returns:
        The indices of the bounding boxes to keep.
    """
    indices = cv2.dnn.NMSBoxes(
        bboxes, scores, score_threshold=0.0, nms_threshold=iou_thresh
    )
    return np.array(indices, dtype=np.int32)
