"""Basic pixel-wise operations.

Functions here work independently on each pixel without considering neighbors.
Includes operations like:
- Inversion (negative images)
- Arithmetic (add, subtract, multiply, divide)
- Bitwise logic (AND, OR, XOR, NOT)
- Thresholding and normalization
"""


def _import_cpp():  # noqa
    from nextcv._cpp.nextcv_py import image as _cpp_image  # noqa

    return _cpp_image


# Import the C++ linalg module
_cpp_image = _import_cpp()

# Expose the matvec function
invert = _cpp_image.invert
