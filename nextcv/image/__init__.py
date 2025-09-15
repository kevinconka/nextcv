"""NextCV Image module - Image processing functionality."""

from nextcv._cpp import image as _cpp_image

invert = _cpp_image.invert

__all__ = ["invert"]
