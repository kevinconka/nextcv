"""Legacy build configuration for NextCV package.

This setup script provides backward compatibility for Python 3.6+ environments.
It uses scikit-build for CMake integration and setuptools-scm for versioning.

Build Commands:
    # Copy legacy build configuration
    cp pyproject.legacy.toml pyproject.toml

    # Build wheel package
    pip wheel --no-deps .

    # Install in development mode
    pip install -e .

Note:
    For modern Python environments (3.9+), use pyproject.toml directly with
    scikit-build-core instead.
"""

import os

from setuptools import find_packages
from skbuild import setup  # This line replaces 'from setuptools import setup'

# Set custom build and dist directories for scikit-build
os.environ.setdefault("SKBUILD_BUILD_DIR", "build")
os.environ.setdefault("SKBUILD_DIST_DIR", "dist")

setup(
    name="nextcv",
    description="Python-first computer vision library with C++ bdingings for speed.",
    use_scm_version=True,  # ← dynamic versioning
    setup_requires=["setuptools-scm"],  # ← required before build
    packages=find_packages(include=["nextcv*"]),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "opencv-python>=4.4.0",
    ],
)
