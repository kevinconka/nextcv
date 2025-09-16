"""NextCV Linear Algebra module - Linear algebra functionality using Eigen."""

from __future__ import annotations

from typing import TYPE_CHECKING

from nextcv._cpp.nextcv_py.linalg import matvec as _matvec

if TYPE_CHECKING:
    from numpy.typing import NDArray


def matvec(matrix: NDArray, vector: NDArray) -> NDArray:
    """Multiply matrix (MxN) by vector (N) → y (M). Uses Eigen.

    Args:
        matrix: Input matrix of shape (M, N)
        vector: Input vector of shape (N,)

    Returns:
        Result vector of shape (M,)
    """
    return _matvec(matrix, vector)


__all__ = ["matvec"]
