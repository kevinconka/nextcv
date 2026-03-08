"""Post-processing utilities."""

from __future__ import annotations

import typing

import numpy
import numpy.typing

__all__: list[str] = ["nms", "weighted_boxes_fusion"]

def nms(
    bboxes: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, n]"],
    scores: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"],
    threshold: typing.SupportsFloat = 0.5,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
    """Apply Non-Maximum Suppression to bounding boxes (numpy arrays)."""

def weighted_boxes_fusion(
    boxes_list: list[typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 4]"]],
    scores_list: list[
        typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"]
    ],
    labels_list: list[typing.Annotated[numpy.typing.ArrayLike, numpy.int32, "[m, 1]"]],
    weights: list[typing.SupportsFloat] = ...,
    iou_thr: typing.SupportsFloat = 0.55,
    skip_box_thr: typing.SupportsFloat = 0.0,
    conf_type: str = "avg",
    allows_overflow: bool = False,
) -> tuple[
    typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, 4]"],
    typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, 1]"],
    typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"],
]:
    """Apply Weighted Box Fusion to per-model detections."""
