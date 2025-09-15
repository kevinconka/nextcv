"""NextCV Linear Algebra module - Linear algebra functionality using Eigen."""

from nextcv._cpp import linalg as _cpp_linalg

matvec = _cpp_linalg.matvec

__all__ = ["matvec"]
