import numpy as np
from numpy.typing import NDArray

def hello() -> str:
    """Return a greeting message from the C++ implementation."""
    ...

def invert(pixels: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Invert the pixel values of a uint8 numpy array.

    Args:
        pixels: Input array of uint8 values to invert.

    Returns:
        NDArray[np.uint8]: Inverted array where each value is (255 - original_value).
    """
    ...

def nms(
    bboxes: NDArray[np.float32], scores: NDArray[np.float32], threshold: float = 0.5
) -> NDArray[np.int32]:
    """Apply Non-Maximum Suppression to bounding boxes.

    Args:
        bboxes: Bounding boxes as (N, 4) array with (x1, y1, x2, y2) format
        scores: Confidence scores as (N,) array
        threshold: IoU threshold for suppression (default: 0.5)

    Returns:
        NDArray[np.int32]: Indices of boxes to keep
    """
    ...

__all__ = ["hello", "invert", "nms"]
