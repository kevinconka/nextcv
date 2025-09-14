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
from . import core, image, postprocessing
from .core import hello_cpp, hello_python

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["core", "image", "postprocessing", "hello_cpp", "hello_python"]
