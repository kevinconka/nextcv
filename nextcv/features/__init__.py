"""NextCV Features module - Feature detection and matching.

This module provides feature detection functions (currently Python-only, 
C++ implementations can be added in the future).
"""

def detect_corners_python(image, threshold=0.01):
    """Python implementation of corner detection (simplified).
    
    Args:
        image: Input image as numpy array
        threshold: Corner response threshold
        
    Returns:
        List of corner coordinates as (x, y) tuples
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required for this function. Install with: pip install numpy")
    
    # This is a very simplified corner detection
    # In practice, you'd use more sophisticated algorithms like Harris corner detection
    if len(image.shape) == 3:
        gray = np.mean(image, axis=2)
    else:
        gray = image
    
    # Simple gradient-based corner detection
    grad_x = np.gradient(gray, axis=1)
    grad_y = np.gradient(gray, axis=0)
    
    # Corner response (simplified)
    corner_response = grad_x**2 + grad_y**2
    
    # Find corners above threshold
    corners = np.where(corner_response > threshold * corner_response.max())
    
    return list(zip(corners[1], corners[0]))  # Return as (x, y) tuples

# For now, only Python implementation is available
detect_corners = detect_corners_python

__all__ = [
    "detect_corners", "detect_corners_python"
]