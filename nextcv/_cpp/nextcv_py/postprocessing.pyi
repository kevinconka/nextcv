"""Post-processing utilities."""

from __future__ import annotations

import typing

import numpy
import numpy.typing

__all__: list[str] = ["nms"]

def nms(
    bboxes: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, n]"],
    scores: typing.Annotated[numpy.typing.ArrayLike, numpy.float32, "[m, 1]"],
    threshold: typing.SupportsFloat = 0.5,
) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
    """Apply Non-Maximum Suppression to bounding boxes (numpy arrays)."""
