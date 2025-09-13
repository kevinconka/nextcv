"""NextCV Image module - Image processing functionality.

This module provides image processing functions with both C++ and Python implementations.
"""

# Try to import C++ wrapped functions
try:
    from .._internal.nextcv_py import invert as _invert_cpp, threshold as _threshold_cpp
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

# Python implementations
def invert_python(image):
    """Python implementation of image inversion.
    
    Args:
        image: Input image as numpy array
        
    Returns:
        Inverted image as numpy array
    """
    try:
        import numpy as np
        return 255 - image
    except ImportError:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")

def threshold_python(image, threshold_val, max_value=255):
    """Python implementation of binary thresholding.
    
    Args:
        image: Input image as numpy array
        threshold_val: Threshold value (0-255)
        max_value: Value to assign to pixels above threshold
        
    Returns:
        Thresholded image as numpy array
    """
    try:
        import numpy as np
        return np.where(image > threshold_val, max_value, 0)
    except ImportError:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")

# Expose functions with C++ as default, Python as fallback
if CPP_AVAILABLE:
    invert = _invert_cpp
    threshold = _threshold_cpp
else:
    invert = invert_python
    threshold = threshold_python

# Always expose both implementations
__all__ = [
    "invert", "invert_python",
    "threshold", "threshold_python"
]