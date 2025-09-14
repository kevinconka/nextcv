"""NextCV Core module - Core functionality."""

from nextcv._internal.nextcv_py import hello as hello_cpp


# Python implementation
def hello_python() -> str:
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"


__all__ = ["hello_python", "hello_cpp"]
