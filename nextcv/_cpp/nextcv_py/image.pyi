"""Image processing utilities."""

from __future__ import annotations

import typing

import numpy
import numpy.typing

__all__: list[str] = ["invert"]

def invert(
    arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8],
) -> numpy.typing.NDArray[numpy.uint8]:
    """Invert n-dimensional array of 8-bit pixels, preserving shape."""
