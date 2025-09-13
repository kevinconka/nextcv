"""NextCV Utils module - Utility functions.

This module provides utility functions implemented in pure Python.
"""

def load_image(filepath):
    """Load an image from file using PIL.
    
    Args:
        filepath: Path to the image file
        
    Returns:
        Image as numpy array (H, W, C) with uint8 dtype
        
    Raises:
        ImportError: If PIL/Pillow is not installed
        FileNotFoundError: If image file doesn't exist
    """
    try:
        import numpy as np
        from PIL import Image
        from pathlib import Path
    except ImportError as e:
        raise ImportError(f"Required dependencies not available: {e}")
    
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

def save_image(image, filepath, quality=95):
    """Save an image to file using PIL.
    
    Args:
        image: Image as numpy array (H, W, C) with uint8 dtype
        filepath: Path where to save the image
        quality: JPEG quality (1-100), ignored for other formats
        
    Raises:
        ImportError: If PIL/Pillow is not installed
    """
    try:
        import numpy as np
        from PIL import Image
        from pathlib import Path
    except ImportError as e:
        raise ImportError(f"Required dependencies not available: {e}")
    
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

def resize_image(image, size, method='bilinear'):
    """Resize an image using numpy operations.
    
    Args:
        image: Input image as numpy array (H, W, C)
        size: Target size as int (square) or (width, height) tuple
        method: Resize method ('nearest', 'bilinear')
        
    Returns:
        Resized image as numpy array
    """
    try:
        import numpy as np
    except ImportError:
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

def normalize_image(image, min_val=0.0, max_val=1.0):
    """Normalize image to specified range.
    
    Args:
        image: Input image as numpy array
        min_val: Minimum value of output range
        max_val: Maximum value of output range
        
    Returns:
        Normalized image as float array
    """
    try:
        import numpy as np
    except ImportError:
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

def validate_image(image):
    """Validate that an array is a valid image.
    
    Args:
        image: Input array to validate
        
    Returns:
        True if valid image, False otherwise
    """
    try:
        import numpy as np
        if not isinstance(image, np.ndarray):
            return False
        
        if image.ndim not in [2, 3]:
            return False
        
        if image.dtype not in [np.uint8, np.uint16, np.float32, np.float64]:
            return False
        
        if image.size == 0:
            return False
        
        return True
    except ImportError:
        # Basic validation without numpy
        return hasattr(image, '__len__') and len(image) > 0

def draw_boxes(image, boxes, labels=None, colors=None):
    """Draw bounding boxes on an image.
    
    Args:
        image: Input image as numpy array (H, W, C)
        boxes: List of bounding boxes as (x, y, width, height) tuples
        labels: Optional list of labels for each box
        colors: Optional list of colors for each box
        
    Returns:
        Image with drawn boxes as numpy array
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    
    # Create a copy to avoid modifying the original
    result = image.copy()
    
    if not boxes:
        return result
    
    # Default colors
    if colors is None:
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    
    # Draw each box
    for i, (x, y, w, h) in enumerate(boxes):
        color = colors[i % len(colors)]
        
        # Convert to integer coordinates
        x, y, w, h = int(x), int(y), int(w), int(h)
        
        # Draw rectangle (simplified - just draw lines)
        # Top and bottom edges
        if y >= 0 and y < result.shape[0]:
            result[y, x:x+w] = [255, 0, 0] if color == 'red' else [0, 0, 255]
        if y+h-1 >= 0 and y+h-1 < result.shape[0]:
            result[y+h-1, x:x+w] = [255, 0, 0] if color == 'red' else [0, 0, 255]
        
        # Left and right edges
        if x >= 0 and x < result.shape[1]:
            result[y:y+h, x] = [255, 0, 0] if color == 'red' else [0, 0, 255]
        if x+w-1 >= 0 and x+w-1 < result.shape[1]:
            result[y:y+h, x+w-1] = [255, 0, 0] if color == 'red' else [0, 0, 255]
    
    return result

__all__ = [
    "load_image", "save_image", "resize_image", "normalize_image", 
    "validate_image", "draw_boxes"
]