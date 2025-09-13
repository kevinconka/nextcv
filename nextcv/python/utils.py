"""Pure Python utility functions for NextCV.

This module provides utility functions implemented in pure Python,
typically for data processing, validation, and convenience functions.
"""

from typing import Union, Tuple, Optional

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
        
        @staticmethod
        def clip(array, min_val, max_val):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        @staticmethod
        def linspace(start, stop, num):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        @staticmethod
        def round(array):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        @staticmethod
        def ix_(*args):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        uint8 = "uint8"
        float32 = "float32"


def resize_image(image, size: Union[int, Tuple[int, int]], 
                method: str = 'bilinear'):
    """Resize an image using numpy operations.
    
    Args:
        image: Input image as numpy array (H, W, C)
        size: Target size as int (square) or (width, height) tuple
        method: Resize method ('nearest', 'bilinear')
        
    Returns:
        Resized image as numpy array
        
    Note:
        This is a simple implementation for demonstration.
        For production use, consider using scipy.ndimage or PIL.
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    if isinstance(size, int):
        size = (size, size)
    
    h, w = image.shape[:2]
    new_w, new_h = size
    
    if method == 'nearest':
        # Simple nearest neighbor resize
        y_indices = np.round(np.linspace(0, h-1, new_h)).astype(int)
        x_indices = np.round(np.linspace(0, w-1, new_w)).astype(int)
        
        if len(image.shape) == 3:
            resized = image[np.ix_(y_indices, x_indices)]
        else:
            resized = image[np.ix_(y_indices, x_indices)]
    else:
        # Simple bilinear resize (simplified)
        y_indices = np.linspace(0, h-1, new_h)
        x_indices = np.linspace(0, w-1, new_w)
        
        # This is a very simplified version - real bilinear would be more complex
        y_indices = np.round(y_indices).astype(int)
        x_indices = np.round(x_indices).astype(int)
        
        if len(image.shape) == 3:
            resized = image[np.ix_(y_indices, x_indices)]
        else:
            resized = image[np.ix_(y_indices, x_indices)]
    
    return resized


def normalize_image(image, 
                   min_val: float = 0.0, 
                   max_val: float = 1.0):
    """Normalize image to specified range.
    
    Args:
        image: Input image as numpy array
        min_val: Minimum value of output range
        max_val: Maximum value of output range
        
    Returns:
        Normalized image as float array
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    # Convert to float
    img_float = image.astype(np.float32)
    
    # Normalize to [0, 1]
    img_min = img_float.min()
    img_max = img_float.max()
    
    if img_max > img_min:
        normalized = (img_float - img_min) / (img_max - img_min)
    else:
        normalized = np.zeros_like(img_float)
    
    # Scale to desired range
    normalized = normalized * (max_val - min_val) + min_val
    
    return normalized


def validate_image(image) -> bool:
    """Validate that an array is a valid image.
    
    Args:
        image: Input array to validate
        
    Returns:
        True if valid image, False otherwise
    """
    if not NUMPY_AVAILABLE:
        # Basic validation without numpy
        return hasattr(image, '__len__') and len(image) > 0
    if not isinstance(image, np.ndarray):
        return False
    
    if image.ndim not in [2, 3]:
        return False
    
    if image.dtype not in [np.uint8, np.uint16, np.float32, np.float64]:
        return False
    
    if image.size == 0:
        return False
    
    return True