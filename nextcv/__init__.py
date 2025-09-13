"""NextCV: Computer Vision library with C++ backend and Python bindings."""

from importlib.metadata import PackageNotFoundError, version

from .nextcv_py import hello, invert

try:
    __version__ = version("nextcv")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["hello", "invert"]
