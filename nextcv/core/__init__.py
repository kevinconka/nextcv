"""NextCV Core module - Core functionality."""

from nextcv._cpp import core as _core_cpp

hello_cpp = _core_cpp.hello


def hello_python() -> str:
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"


__all__ = ["hello_python", "hello_cpp"]
