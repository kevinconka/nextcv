"""Linear algebra utilities."""

from __future__ import annotations

import typing

import numpy
import numpy.typing

__all__: list[str] = ["matvec"]

def matvec(
    matrix: typing.Annotated[
        numpy.typing.NDArray[numpy.float32], "[m, n]", "flags.f_contiguous"
    ],
    vector: typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, 1]"],
) -> typing.Annotated[numpy.typing.NDArray[numpy.float32], "[m, 1]"]:
    """Multiply matrix (MxN) by vector (N) → y (M). Uses Eigen."""
