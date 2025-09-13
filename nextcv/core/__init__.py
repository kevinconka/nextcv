"""NextCV Core module - Core utilities and base functionality.

This module provides core functionality with both C++ and Python implementations.
"""

# Try to import C++ wrapped functions
try:
    from .._internal.nextcv_py import hello as _hello_cpp, get_version as _get_version_cpp, get_build_info as _get_build_info_cpp
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

# Python implementations
def hello_python():
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"

def get_version_python():
    """Python implementation of get_version function."""
    return "0.1.0 (Python-only mode)"

def get_build_info_python():
    """Python implementation of get_build_info function."""
    return "NextCV 0.1.0 - Python-only mode (C++ bindings not built)"

# Expose functions with C++ as default, Python as fallback
if CPP_AVAILABLE:
    hello = _hello_cpp
    get_version = _get_version_cpp
    get_build_info = _get_build_info_cpp
else:
    hello = hello_python
    get_version = get_version_python
    get_build_info = get_build_info_python

# Always expose both implementations
__all__ = [
    "hello", "hello_python",
    "get_version", "get_version_python", 
    "get_build_info", "get_build_info_python"
]