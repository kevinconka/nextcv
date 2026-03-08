"""Post-processing utilities."""

from __future__ import annotations

import collections.abc
import typing

import numpy
import numpy.typing

__all__: list[str] = ["nms", "wbf", "weighted_boxes_fusion"]

def nms(
    bboxes: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, n]"],
    scores: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"],
    threshold: typing.SupportsFloat | typing.SupportsIndex = 0.5,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
    """Apply Non-Maximum Suppression to bounding boxes (numpy arrays)."""

def wbf(
    boxes_list: collections.abc.Sequence[
        collections.abc.Sequence[
            typing.Annotated[
                collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex],
                "FixedSize(4)",
            ]
        ]
    ],
    scores_list: collections.abc.Sequence[
        collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]
    ],
    labels_list: collections.abc.Sequence[
        collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]
    ],
    weights: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex] = [],
    iou_thr: typing.SupportsFloat | typing.SupportsIndex = 0.550000011920929,
    skip_box_thr: typing.SupportsFloat | typing.SupportsIndex = 0.0,
    conf_type: str = "avg",
    allows_overflow: bool = False,
) -> tuple[list[typing.Annotated[list[float], "FixedSize(4)"]], list[float], list[int]]:
    """Apply Weighted Box Fusion to per-model detections."""

def weighted_boxes_fusion(
    boxes_list: collections.abc.Sequence[
        collections.abc.Sequence[
            typing.Annotated[
                collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex],
                "FixedSize(4)",
            ]
        ]
    ],
    scores_list: collections.abc.Sequence[
        collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]
    ],
    labels_list: collections.abc.Sequence[
        collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]
    ],
    weights: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex] = [],
    iou_thr: typing.SupportsFloat | typing.SupportsIndex = 0.550000011920929,
    skip_box_thr: typing.SupportsFloat | typing.SupportsIndex = 0.0,
    conf_type: str = "avg",
    allows_overflow: bool = False,
) -> tuple[list[typing.Annotated[list[float], "FixedSize(4)"]], list[float], list[int]]:
    """Apply Weighted Box Fusion to per-model detections."""
