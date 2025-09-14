"""NextCV Core module - Core functionality."""

# Try to import C++ wrapped functions
try:
    from .._internal.nextcv_py import hello as _hello_cpp
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

# Python implementation
def hello_python():
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"

# Expose functions with C++ as default, Python as fallback
if CPP_AVAILABLE:
    hello = _hello_cpp
else:
    hello = hello_python

__all__ = ["hello", "hello_python"]