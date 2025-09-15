"""Basic pixel-wise operations.

Functions here work independently on each pixel without considering neighbors.
Includes operations like:
- Inversion (negative images)
- Arithmetic (add, subtract, multiply, divide)
- Bitwise logic (AND, OR, XOR, NOT)
- Thresholding and normalization
"""


def _import_cpp():  # noqa
    from nextcv._cpp.nextcv_py import invert as _invert  # noqa

    return _invert


invert = _import_cpp()
