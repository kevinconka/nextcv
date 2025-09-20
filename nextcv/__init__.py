"""NextCV: Computer Vision library with C++ and Python implementations.

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

from importlib.metadata import PackageNotFoundError, version

# Import modules
from . import core, image, linalg, postprocessing

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["core", "image", "postprocessing", "linalg"]
__all__ += core.__all__
