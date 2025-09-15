import numpy as np
from numpy.typing import NDArray

# Core submodule
class core:
    """Core utilities."""

    @staticmethod
    def hello() -> str:
        """Return a greeting from NextCV C++."""
        ...

# Image processing submodule
class image:
    """Image processing utilities."""

    @staticmethod
    def invert(pixels: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """Invert n-dimensional array of 8-bit pixels, preserving shape.

        Args:
            pixels: Input array of uint8 values to invert.

        Returns:
            NDArray[np.uint8]: Inverted array where each value is (255 - value).
        """
        ...

# Post-processing submodule
class postprocessing:
    """Post-processing utilities."""

    @staticmethod
    def nms(
        bboxes: NDArray[np.float32], scores: NDArray[np.float32], threshold: float = 0.5
    ) -> NDArray[np.int32]:
        """Apply Non-Maximum Suppression to bounding boxes (numpy arrays).

        Args:
            bboxes: Bounding boxes as (N, 4) array with (x1, y1, x2, y2) format
            scores: Confidence scores as (N,) array
            threshold: IoU threshold for suppression (default: 0.5)

        Returns:
            NDArray[np.int32]: Indices of boxes to keep
        """
        ...

# Linear algebra submodule
class linalg:
    """Linear algebra utilities."""

    @staticmethod
    def matvec(A: NDArray[np.float32], x: NDArray[np.float32]) -> NDArray[np.float32]:
        """Multiply matrix A (M×N) by vector x (N) → y (M). Uses Eigen.

        Args:
            A: Input matrix of shape (M, N) with float32 dtype
            x: Input vector of shape (N,) with float32 dtype

        Returns:
            NDArray[np.float32]: Result vector of shape (M,) with float32 dtype

        Raises:
            ValueError: If matrix and vector dimensions don't match
        """
        ...

__all__ = ["core", "image", "postprocessing", "linalg"]
