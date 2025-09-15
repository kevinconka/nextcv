# Testing & Debugging

Essential testing strategy for NextCV C++-Python bindings.

## Essential Tests

### Test Both Implementations

```python
import numpy as np
import nextcv.postprocessing as pp

def test_nms_implementations():
    """Test that C++ and Python NMS produce the same result."""
    bboxes = np.array([
        [10, 10, 50, 50],   # Box 0
        [15, 15, 55, 55],   # Box 1 (overlaps with 0)
        [100, 100, 150, 150] # Box 2 (separate)
    ], dtype=np.float32)

    scores = np.array([0.9, 0.8, 0.7], dtype=np.float32)

    # Compare implementations
    result_cpp = pp.nms_cpp(bboxes, scores, 0.5)
    result_py = pp.nms_np(bboxes, scores, 0.5)
    np.testing.assert_array_equal(result_cpp, result_py)
```

### Test Edge Cases

```python
def test_edge_cases():
    """Test empty and single inputs."""
    # Empty input
    empty_bboxes = np.array([], dtype=np.float32).reshape(0, 4)
    empty_scores = np.array([], dtype=np.float32)
    result = pp.nms_np(empty_bboxes, empty_scores, 0.5)
    assert len(result) == 0

    # Single box
    single_bbox = np.array([[10, 10, 50, 50]], dtype=np.float32)
    single_score = np.array([0.9], dtype=np.float32)
    result = pp.nms_np(single_bbox, single_score, 0.5)
    assert len(result) == 1
```

### Test Image Operations

```python
import nextcv.image.ops as ops

def test_invert_function():
    """Test image inversion."""
    image = np.array([[[255, 0, 0], [0, 255, 0]]], dtype=np.uint8)
    inverted = ops.invert(image)

    assert inverted.shape == image.shape
    assert inverted[0, 0, 0] == 0  # 255 -> 0
```

## Debugging Tips

### Use Python Fallbacks

```python
# Force Python implementation for debugging
pp.nms_cpp = None
result = pp.nms_np(bboxes, scores, 0.5)  # Uses Python only
```

### Test Invalid Inputs

```python
import pytest

def test_invalid_inputs():
    """Test error handling."""
    bboxes = np.array([[10, 10, 50, 50]], dtype=np.float32)
    scores = np.array([0.9], dtype=np.float32)

    # Wrong number of scores
    with pytest.raises(ValueError):
        pp.nms_np(bboxes, scores[:0], 0.5)
```

## Common Issues

- **Memory Leaks** - Use RAII in C++ and proper NumPy handling
- **Type Mismatches** - Validate `dtype` and `shape` before processing
- **Performance Regression** - Profile with `%timeit` in Jupyter
- **Bounding Box Format** - Always use (x1, y1, x2, y2) format

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific module
pytest tests/postprocessing/

# Run specific test
pytest tests/postprocessing/test_boxes.py::test_nms_np
```

## Pro Tips

- **Compare all implementations** - C++, Python, and OpenCV
- **Test edge cases** - Empty boxes, single boxes, overlapping boxes
- **Use Python fallbacks** - Debug complex logic in Python first
- **Profile performance** - Ensure C++ actually helps
