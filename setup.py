"""Legacy build configuration for NextCV package.

This setup script provides backward compatibility for Python 3.6+ environments.
It uses scikit-build for CMake integration and setuptools-scm for versioning.

Build Commands:
    # Copy legacy build configuration
    cp pyproject.legacy.toml pyproject.toml

    # Build wheel package
    pip wheel --no-deps -w dist .

    # Install in development mode
    pip install -e ".[dev]"

Note:
    For modern Python environments (3.9+), use pyproject.toml directly with
    scikit-build-core instead.
"""

from setuptools import find_packages
from skbuild import setup  # This line replaces 'from setuptools import setup'

setup(
    name="nextcv",
    description="Python-first computer vision library with C++ bdingings for speed.",
    use_scm_version=True,  # ← dynamic versioning
    setup_requires=["setuptools-scm"],  # ← required before build
    packages=find_packages(include=["nextcv*"]),
    python_requires=">=3.6",
    install_requires=[
        "numpy<1.19.5; python_version == '3.6'",
        "numpy>=1.19.0; python_version > '3.6'",
        "opencv-python-headless<4.7; python_version < '3.8'",
        "opencv-python-headless>=4.4; python_version >= '3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=7",
            "pytest-cov>=4.0",
        ]
    },
)
