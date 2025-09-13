"""NextCV: Computer Vision library with mixed C++ and Python implementations.

This package provides both high-performance C++ wrapped functions and
pure Python implementations in the same modules, allowing you to choose
the best implementation for your needs.

Usage:
    # Mixed modules - C++ as default, Python as fallback
    from nextcv.image import invert, invert_python
    from nextcv.postprocessing import nms, fast_nms, nms_python
    
    # Core functionality
    from nextcv.core import hello, get_version
    
    # Utilities (Python-only)
    from nextcv.utils import load_image, save_image, draw_boxes
    
    # Features (Python-only for now)
    from nextcv.features import detect_corners
"""

from importlib.metadata import PackageNotFoundError, version

# Import from mixed modules
from .core import hello, get_version, get_build_info
from .image import invert, threshold
from .postprocessing import nms, fast_nms
from .utils import load_image, save_image, resize_image, normalize_image, validate_image, draw_boxes
from .features import detect_corners

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

# All available functions
__all__ = [
    # Core
    "hello", "get_version", "get_build_info",
    # Image processing
    "invert", "threshold", 
    # Post-processing
    "nms", "fast_nms",
    # Utilities
    "load_image", "save_image", "resize_image", "normalize_image", "validate_image", "draw_boxes",
    # Features
    "detect_corners"
]
