"""NextCV API module - C++ wrapped functionality.

This module contains all functions that are implemented in C++ and wrapped
with pybind11 for high performance.

Usage:
    import nextcv.api as api
    result = api.invert(image)
    
    # Or import specific functions
    from nextcv.api import invert, threshold, nms
"""

try:
    from .._internal.nextcv_py import hello, invert, threshold, nms, get_version, get_build_info
    __all__ = ["hello", "invert", "threshold", "nms", "get_version", "get_build_info"]
except ImportError:
    # C++ bindings not available
    def hello():
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    def invert(image):
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    def threshold(image, threshold_val, max_value=255):
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    def nms(boxes, threshold=0.5):
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    def get_version():
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    def get_build_info():
        raise NotImplementedError("C++ bindings not available. Build the project to enable C++ functions.")
    
    __all__ = ["hello", "invert", "threshold", "nms", "get_version", "get_build_info"]