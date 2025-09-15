"""Linear algebra operations using Eigen.

Functions here provide high-performance linear algebra operations using the Eigen library.
Includes operations like:
- Matrix-vector multiplication
- Matrix-matrix multiplication (future)
- Linear system solving (future)
- Eigenvalue decomposition (future)
"""


def _import_cpp():  # noqa
    from nextcv._cpp.nextcv_py import linalg as _cpp_linalg  # noqa

    return _cpp_linalg


# Import the C++ linalg module
_cpp_linalg = _import_cpp()

# Expose the matvec function
matvec = _cpp_linalg.matvec