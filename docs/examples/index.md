# NextCV Examples

Welcome to the NextCV examples! Here you'll find practical examples showing how to use NextCV for real computer vision tasks.

## 🚀 Quick Examples

### Basic Image Processing

```python
import numpy as np
import nextcv as cvx

# Create a sample image
image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

# Invert the image
inverted = cvx.image.invert(image)
print(f"Original shape: {image.shape}")
print(f"Inverted shape: {inverted.shape}")
```

### Object Detection Post-Processing

```python
import numpy as np
import nextcv as cvx

# Simulate detection results
boxes = np.array([
    [10, 10, 50, 50],   # x1, y1, x2, y2
    [20, 20, 60, 60],   # Overlapping box
    [100, 100, 150, 150], # Non-overlapping box
], dtype=np.float32)

scores = np.array([0.9, 0.8, 0.7], dtype=np.float32)

# Apply Non-Maximum Suppression
filtered_boxes = cvx.postprocessing.nms_cpp(boxes, scores, threshold=0.5)
print(f"Original boxes: {len(boxes)}")
print(f"Filtered boxes: {len(filtered_boxes)}")
```

## 📊 Performance Benchmarks

### Image Inversion Speed Test

```python
import timeit
import numpy as np
import nextcv as cvx

# Create test image
image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)

# Time C++ implementation
t_cpp = timeit.timeit(
    "cvx.image.invert_cpp(image)", 
    globals=globals(), 
    number=10
)

# Time Python implementation (if available)
t_py = timeit.timeit(
    "cvx.image.invert_python(image)", 
    globals=globals(), 
    number=10
)

print(f"C++ invert: {t_cpp:.3f} seconds")
print(f"Python invert: {t_py:.3f} seconds")
print(f"Speedup: {t_py/t_cpp:.1f}x")
```

### NMS Performance Comparison

```python
import timeit
import numpy as np
import nextcv as cvx

# Create test data
N = 1000
rng = np.random.default_rng(42)
boxes = rng.uniform(0, 100, (N, 4)).astype(np.float32)
scores = rng.uniform(0.1, 1, N).astype(np.float32)

# Time implementations
t_cpp = timeit.timeit(
    "cvx.postprocessing.nms_cpp(boxes, scores, 0.5)", 
    globals=globals(), 
    number=100
)

t_py = timeit.timeit(
    "cvx.postprocessing.nms_np(boxes, scores, 0.5)", 
    globals=globals(), 
    number=100
)

print(f"C++ NMS: {t_cpp:.2f} ms/call")
print(f"Python NMS: {t_py:.2f} ms/call")
print(f"Speedup: {t_py/t_cpp:.1f}x")
```

## 🎯 Real-World Use Cases

### Image Preprocessing Pipeline

```python
import numpy as np
import nextcv as cvx

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess image for computer vision tasks."""
    # Convert to grayscale if needed
    if image.ndim == 3:
        # Simple grayscale conversion
        gray = np.mean(image, axis=2).astype(np.uint8)
    else:
        gray = image
    
    # Invert if needed (for certain datasets)
    if should_invert:
        gray = cvx.image.invert(gray)
    
    return gray

# Example usage
image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
processed = preprocess_image(image)
```

### Object Detection Pipeline

```python
import numpy as np
import nextcv as cvx

def detect_objects(image: np.ndarray, model_outputs: dict) -> list:
    """Process model outputs and apply NMS."""
    # Extract boxes and scores from model output
    boxes = model_outputs['boxes']  # Shape: (N, 4)
    scores = model_outputs['scores']  # Shape: (N,)
    
    # Apply NMS
    filtered_indices = cvx.postprocessing.nms_cpp(boxes, scores, threshold=0.5)
    
    # Return filtered results
    return {
        'boxes': boxes[filtered_indices],
        'scores': scores[filtered_indices]
    }

# Example usage
model_outputs = {
    'boxes': np.random.uniform(0, 100, (100, 4)).astype(np.float32),
    'scores': np.random.uniform(0.1, 1, 100).astype(np.float32)
}

results = detect_objects(image, model_outputs)
print(f"Detected {len(results['boxes'])} objects")
```

## 🔧 Development Examples

### Adding Custom Image Processing

```python
# Example of how to add your own image processing function
def custom_image_filter(image: np.ndarray) -> np.ndarray:
    """Custom image processing using NextCV functions."""
    # Use NextCV's invert function
    inverted = cvx.image.invert(image)
    
    # Add your custom processing here
    # ... custom logic ...
    
    return inverted
```

### Error Handling

```python
import nextcv as cvx

def safe_image_processing(image: np.ndarray) -> np.ndarray:
    """Safely process image with error handling."""
    try:
        # Ensure image is the right type
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        # Ensure C-contiguous
        if not image.flags.c_contiguous:
            image = np.ascontiguousarray(image)
        
        # Process image
        result = cvx.image.invert(image)
        return result
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return image  # Return original on error
```

## 🎓 Learning Resources

- **[Getting Started Guide](getting-started.md)** - Basic usage
- **[PyBind11 Guide](pybind11-guide.md)** - Adding new functions
- **[API Reference](reference/)** - Complete API documentation

## 🤝 Contributing Examples

Have a cool example? We'd love to see it! Check out our [contribution guidelines](pybind11-guide.md) to learn how to add your examples to NextCV.

---

<div align="center">

**Ready to build something amazing?** 🚀

[Get Started](getting-started.md) • [View API](reference/) • [Contribute](pybind11-guide.md)

</div>