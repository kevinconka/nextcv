"""Pure Python I/O functions for NextCV.

This module provides image I/O functionality implemented in pure Python,
using standard libraries like PIL/Pillow.
"""

from typing import Union, Tuple, Optional
from pathlib import Path

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Create a dummy numpy-like object for type hints
    class np:
        @staticmethod
        def array(data, dtype=None):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        uint8 = "uint8"

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def load_image(filepath: Union[str, Path]):
    """Load an image from file using PIL.
    
    Args:
        filepath: Path to the image file
        
    Returns:
        Image as numpy array (H, W, C) with uint8 dtype
        
    Raises:
        ImportError: If PIL/Pillow is not installed
        FileNotFoundError: If image file doesn't exist
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    if not PIL_AVAILABLE:
        raise ImportError("PIL/Pillow is required for image I/O. Install with: pip install Pillow")
    
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Image file not found: {filepath}")
    
    with Image.open(filepath) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array
        array = np.array(img)
        
    return array


def save_image(image, filepath: Union[str, Path], 
               quality: int = 95) -> None:
    """Save an image to file using PIL.
    
    Args:
        image: Image as numpy array (H, W, C) with uint8 dtype
        filepath: Path where to save the image
        quality: JPEG quality (1-100), ignored for other formats
        
    Raises:
        ImportError: If PIL/Pillow is not installed
        ValueError: If image format is not supported
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    if not PIL_AVAILABLE:
        raise ImportError("PIL/Pillow is required for image I/O. Install with: pip install Pillow")
    
    filepath = Path(filepath)
    
    # Ensure image is uint8
    if image.dtype != np.uint8:
        image = np.clip(image, 0, 255).astype(np.uint8)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image)
    
    # Save with appropriate quality setting
    if filepath.suffix.lower() in ['.jpg', '.jpeg']:
        pil_image.save(filepath, 'JPEG', quality=quality)
    else:
        pil_image.save(filepath)