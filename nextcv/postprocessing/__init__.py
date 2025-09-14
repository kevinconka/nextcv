"""NextCV Postprocessing module - Post-processing functionality."""

# Try to import C++ wrapped functions
try:
    from .._internal.nextcv_py import nms as _nms_cpp
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

# Python implementation (default)
def nms(boxes, threshold=0.5):
    """Python implementation of Non-Maximum Suppression.
    
    Args:
        boxes: List of bounding boxes as (x, y, width, height, confidence) tuples
        threshold: IoU threshold for suppression
        
    Returns:
        List of filtered bounding boxes
    """
    if not boxes:
        return []
    
    # Sort boxes by confidence (descending)
    sorted_boxes = sorted(boxes, key=lambda x: x[4], reverse=True)
    
    result = []
    suppressed = [False] * len(sorted_boxes)
    
    for i, box1 in enumerate(sorted_boxes):
        if suppressed[i]:
            continue
            
        result.append(box1)
        
        # Suppress boxes with high IoU
        for j in range(i + 1, len(sorted_boxes)):
            if suppressed[j]:
                continue
                
            box2 = sorted_boxes[j]
            
            # Calculate IoU (simplified)
            x1, y1, w1, h1, _ = box1
            x2, y2, w2, h2, _ = box2
            
            # Calculate intersection
            x_left = max(x1, x2)
            y_top = max(y1, y2)
            x_right = min(x1 + w1, x2 + w2)
            y_bottom = min(y1 + h1, y2 + h2)
            
            if x_right < x_left or y_bottom < y_top:
                iou = 0.0
            else:
                intersection = (x_right - x_left) * (y_bottom - y_top)
                area1 = w1 * h1
                area2 = w2 * h2
                union = area1 + area2 - intersection
                iou = intersection / union if union > 0 else 0.0
            
            if iou > threshold:
                suppressed[j] = True
    
    return result

# C++ implementation (if available)
if CPP_AVAILABLE:
    nms_fast = _nms_cpp
else:
    nms_fast = nms  # Fallback to Python

__all__ = ["nms", "nms_fast"]