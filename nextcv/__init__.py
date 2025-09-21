"""NextCV: Python-first computer vision library with C++ bdingings for speed.

This package provides both high-performance C++ wrapped functions and
pure Python implementations in functional modules.

Usage:
    import nextcv as cvx

    # C++ wrapped functions
    cvx.image.invert(image)
    cvx.postprocessing.nms_fast(boxes, 0.5)

    # Python implementations
    cvx.postprocessing.nms(boxes, 0.5)
    cvx.core.hello()
"""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # python 3.6 and 3.7

# Import modules
from . import core, image, linalg, postprocessing

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["core", "image", "postprocessing", "linalg"]
__all__ += core.__all__
