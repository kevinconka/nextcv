"""NextCV Core module - Core functionality."""

from nextcv._cpp.nextcv_py.core import hello as _hello


def hello_cpp() -> str:
    """C++ implementation of hello function."""
    return _hello()


def hello_python() -> str:
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"


__all__ = ["hello_python", "hello_cpp"]
