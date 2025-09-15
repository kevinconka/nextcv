"""Python implementation of hello function."""


def _import_cpp():  # noqa
    from nextcv._cpp.nextcv_py import hello as _hello  # noqa

    return _hello


def hello_python() -> str:
    """Python implementation of hello function."""
    return "Hello from NextCV (Python)"


hello_cpp = _import_cpp()
