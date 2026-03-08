"""Post-processing utilities."""

from __future__ import annotations

import collections.abc
import typing

import numpy
import numpy.typing

__all__: list[str] = ["nms", "weighted_boxes_fusion"]

def nms(
    bboxes: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, n]"],
    scores: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"],
    threshold: typing.SupportsFloat | typing.SupportsIndex = 0.5,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
    """Apply Non-Maximum Suppression to bounding boxes (numpy arrays)."""

def weighted_boxes_fusion(
    boxes_list: collections.abc.Sequence[
        typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, n]"]
    ],
    scores_list: collections.abc.Sequence[
        typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"]
    ],
    labels_list: collections.abc.Sequence[
        typing.Annotated[numpy.typing.ArrayLike, numpy.int32, "[m, 1]"]
    ],
    weights: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex] = [],
    iou_thr: typing.SupportsFloat | typing.SupportsIndex = 0.550000011920929,
    skip_box_thr: typing.SupportsFloat | typing.SupportsIndex = 0.0,
    conf_type: str = "avg",
    allows_overflow: bool = False,
) -> tuple[
    typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, n]"],
    typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, 1]"],
    typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"],
]:
    """Apply Weighted Box Fusion to per-model detections."""
