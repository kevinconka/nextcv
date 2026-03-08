"""
NextCV pybind11 bindings
"""

from __future__ import annotations
from . import core
from . import image
from . import linalg
from . import postprocessing

__all__: list[str] = ["core", "image", "linalg", "postprocessing"]
