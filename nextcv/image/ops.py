"""Image operations.

Functions here modify pixel values without changing image layout.
Includes operations like:
- Pixel-wise arithmetic and logic
- Thresholding and binarization
"""

from typing import TYPE_CHECKING

from nextcv._cpp.nextcv_py.image import invert as _invert

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


def invert(image: "NDArray[np.uint8]") -> "NDArray[np.uint8]":
    """Invert the image."""
    return _invert(image)
