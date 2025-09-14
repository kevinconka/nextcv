"""NextCV Image module - Image processing functionality."""

# Try to import C++ wrapped functions
try:
    from .._internal.nextcv_py import invert as _invert_cpp
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

# Python implementation
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

# Expose functions with C++ as default, Python as fallback
if CPP_AVAILABLE:
    invert = _invert_cpp
else:
    invert = invert_python

__all__ = ["invert", "invert_python"]