"""Pure Python visualization functions for NextCV.

This module provides visualization functions implemented in pure Python,
using matplotlib and other standard libraries.
"""

from typing import List, Tuple, Union, Optional

try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    # Create dummy objects for type hints
    class np:
        @staticmethod
        def array(data, dtype=None):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        @staticmethod
        def ceil(value):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
        
        @staticmethod
        def sqrt(value):
            raise ImportError("numpy is required for this function. Install with: pip install numpy")
    
    class plt:
        @staticmethod
        def subplots(*args, **kwargs):
            raise ImportError("matplotlib is required for this function. Install with: pip install matplotlib")
    
    class patches:
        pass


def draw_boxes(image, 
               boxes: List[Tuple[float, float, float, float]], 
               labels: Optional[List[str]] = None,
               colors: Optional[List[str]] = None):
    """Draw bounding boxes on an image.
    
    Args:
        image: Input image as numpy array (H, W, C)
        boxes: List of bounding boxes as (x, y, width, height) tuples
        labels: Optional list of labels for each box
        colors: Optional list of colors for each box
        
    Returns:
        Image with drawn boxes as numpy array
    """
    if not NUMPY_AVAILABLE:
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


def draw_text(image, 
              text: str, 
              position: Tuple[int, int],
              color: Tuple[int, int, int] = (255, 255, 255),
              font_size: int = 12):
    """Draw text on an image.
    
    Args:
        image: Input image as numpy array (H, W, C)
        text: Text to draw
        position: (x, y) position for text
        color: RGB color tuple
        font_size: Font size (simplified implementation)
        
    Returns:
        Image with drawn text as numpy array
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    # Create a copy to avoid modifying the original
    result = image.copy()
    
    x, y = position
    
    # Simple text drawing (very basic implementation)
    # In a real implementation, you'd use PIL or OpenCV for proper text rendering
    if y >= 0 and y < result.shape[0] and x >= 0 and x < result.shape[1]:
        # This is just a placeholder - real text drawing would be more complex
        # For now, just draw a small rectangle to represent text
        text_width = min(len(text) * font_size // 2, result.shape[1] - x)
        text_height = min(font_size, result.shape[0] - y)
        
        if text_width > 0 and text_height > 0:
            result[y:y+text_height, x:x+text_width] = color
    
    return result


def create_visualization_grid(images: List, 
                             titles: Optional[List[str]] = None,
                             figsize: Tuple[int, int] = (12, 8)):
    """Create a grid visualization of multiple images.
    
    Args:
        images: List of images to display
        titles: Optional list of titles for each image
        figsize: Figure size as (width, height)
        
    Returns:
        Matplotlib figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for this function. Install with: pip install matplotlib")
    n_images = len(images)
    if n_images == 0:
        return None
    
    # Calculate grid dimensions
    cols = int(np.ceil(np.sqrt(n_images)))
    rows = int(np.ceil(n_images / cols))
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1:
        axes = [axes] if cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, img in enumerate(images):
        if i < len(axes):
            axes[i].imshow(img)
            axes[i].axis('off')
            
            if titles and i < len(titles):
                axes[i].set_title(titles[i])
    
    # Hide unused subplots
    for i in range(n_images, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig