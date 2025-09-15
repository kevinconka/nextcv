"""Python implementation of hello function."""


def _import_cpp():  # noqa
    from nextcv._cpp.nextcv_py import core as _core_cpp  # noqa

    return _core_cpp


def hello_python() -> str:
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"


# Import the C++ core module
_core_cpp = _import_cpp()

# Expose the hello function
hello_cpp = _core_cpp.hello
