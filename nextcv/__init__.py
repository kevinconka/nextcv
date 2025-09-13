"""NextCV: Computer Vision library with C++ backend and Python bindings.

This package provides both high-performance C++ wrapped functions and
pure Python utilities for computer vision tasks.

Usage:
    # C++ wrapped functions (high performance)
    import nextcv.api as api
    result = api.invert(image)
    
    # Pure Python functions (utilities, I/O, visualization)
    import nextcv.python as py
    image = py.load_image("image.jpg")
    
    # Convenience imports (both C++ and Python functions)
    import nextcv
    result = nextcv.invert(image)  # C++ wrapped
    image = nextcv.load_image("image.jpg")  # Pure Python
"""

from importlib.metadata import PackageNotFoundError, version

# Import pure Python functions (always available)
from .python.io import load_image, save_image
from .python.utils import resize_image, normalize_image, validate_image
from .python.visualization import draw_boxes, draw_text, create_visualization_grid

# Try to import C++ wrapped functions (only available if built)
try:
    from ._internal.nextcv_py import hello, invert, threshold, nms, get_version, get_build_info
    CPP_AVAILABLE = True
except ImportError:
    # C++ bindings not available - provide placeholder functions
    def hello():
        return "NextCV C++ bindings not available (build required)"
    
    def invert(image):
        raise NotImplementedError("C++ bindings not available. Use nextcv.python for pure Python functions.")
    
    def threshold(image, threshold_val, max_value=255):
        raise NotImplementedError("C++ bindings not available. Use nextcv.python for pure Python functions.")
    
    def nms(boxes, threshold=0.5):
        raise NotImplementedError("C++ bindings not available. Use nextcv.python for pure Python functions.")
    
    def get_version():
        return "0.1.0 (Python-only mode)"
    
    def get_build_info():
        return "NextCV 0.1.0 - Python-only mode (C++ bindings not built)"
    
    CPP_AVAILABLE = False

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

# C++ wrapped functions
__all_cpp__ = ["hello", "invert", "threshold", "nms", "get_version", "get_build_info"]

# Pure Python functions  
__all_python__ = [
    "load_image", "save_image", 
    "resize_image", "normalize_image", "validate_image",
    "draw_boxes", "draw_text", "create_visualization_grid"
]

# All functions (convenience imports)
__all__ = __all_cpp__ + __all_python__
