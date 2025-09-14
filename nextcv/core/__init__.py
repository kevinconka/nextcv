"""NextCV Core module - Core functionality."""

from nextcv._cpp.nextcv_py import hello as hello_cpp

from .hello import hello_python

__all__ = ["hello_python", "hello_cpp"]
