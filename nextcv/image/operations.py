"""Image operations module for NextCV."""

import numpy as np
from .._internal.nextcv_py import invert as _invert, threshold as _threshold


def invert(image: np.ndarray) -> np.ndarray:
    """Invert pixel values in an image.
    
    Args:
        image: Input image as numpy array (any shape, uint8)
        
    Returns:
        Inverted image with same shape as input
        
    Raises:
        RuntimeError: If input array is not C-contiguous
    """
    return _invert(image)


def threshold(image: np.ndarray, threshold_value: int, max_value: int = 255) -> np.ndarray:
    """Apply binary threshold to an image.
    
    Args:
        image: Input image as numpy array (any shape, uint8)
        threshold_value: Threshold value (0-255)
        max_value: Value to assign to pixels above threshold (default: 255)
        
    Returns:
        Thresholded image with same shape as input
        
    Raises:
        RuntimeError: If input array is not C-contiguous
    """
    return _threshold(image, threshold_value, max_value)