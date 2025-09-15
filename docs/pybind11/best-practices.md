# Best Practices

Building maintainable Python-C++ bindings requires following established patterns. Here are the rules that actually matter.

## Naming Conventions

### C++ Functions
```cpp
// Good: snake_case for functions
auto conv2d(const std::vector<float>& input) -> std::vector<float>;
auto gaussian_blur(const Image& image, float sigma) -> Image;

// Good: PascalCase for classes
class ImageProcessor {
public:
    void process_image(const Image& input);
};
```

### Python Functions
```python
# Good: snake_case with suffixes
def conv2d_cpp(image, kernel):
    """C++ implementation."""
    pass

def conv2d_python(image, kernel):
    """Python implementation."""
    pass

def conv2d(image, kernel):
    """Smart wrapper that chooses implementation."""
    pass
```

## Code Organization

### File Structure
```
nextcv/
├── _cpp/src/
│   ├── core/           # Core functionality
│   ├── image/          # Image processing
│   ├── tracking/       # Tracking algorithms
│   └── bindings/       # PyBind11 bindings
├── core/               # Python core modules
├── image/              # Python image modules
└── tracking/           # Python tracking modules
```

### Binding Organization
```cpp
// Group related functions
module.def("conv2d", &conv2d, "Apply 2D convolution");
module.def("gaussian_blur", &gaussian_blur, "Apply Gaussian blur");
module.def("edge_detection", &edge_detection, "Detect edges");
```

## Error Handling

### Input Validation
```cpp
py::array_t<float> my_function(py::array_t<float> input) {
    // Always validate inputs
    if (input.ndim() != 2) {
        throw std::runtime_error("Input must be 2D");
    }

    if (!(input.flags() & py::array::c_style)) {
        throw std::runtime_error("Input must be C-contiguous");
    }

    // Process data...
}
```

### Exception Safety
```cpp
// Use RAII for automatic cleanup
class ImageProcessor {
private:
    std::vector<float> data_;

public:
    ImageProcessor(size_t size) : data_(size) {}
    // Destructor automatically cleans up
};
```

## Memory Management

### Efficient Array Handling
```cpp
py::array_t<float> process_array(py::array_t<float> input) {
    // Get buffer info once
    py::buffer_info buf = input.request();
    float* ptr = static_cast<float*>(buf.ptr);

    // Process in-place when possible
    for (size_t i = 0; i < buf.size; ++i) {
        ptr[i] = process_pixel(ptr[i]);
    }

    return input; // Return same array
}
```

### Avoid Unnecessary Copies
```cpp
// Good: Pass by reference
void process_image(const std::vector<float>& input, std::vector<float>& output);

// Bad: Pass by value
void process_image(std::vector<float> input, std::vector<float> output);
```

## Performance Tips

### Use C-Contiguous Arrays
```cpp
// Always check for C-contiguity
if (!(input.flags() & py::array::c_style)) {
    throw std::runtime_error("Input must be C-contiguous");
}
```

### Optimize Hot Paths
```cpp
// Use const references for large objects
void process_large_data(const std::vector<float>& data) {
    // Process data...
}
```

### Profile Before Optimizing
```python
import cProfile
import nextcv as cvx

# Profile your function
cProfile.run('cvx.tracking.hungarian_algorithm(cost_matrix)')
```

## Documentation

### Function Documentation
```cpp
/**
 * @brief Apply 2D convolution to an image
 * @param input Input image array
 * @param kernel Convolution kernel
 * @return Convolved image array
 */
py::array_t<float> conv2d(py::array_t<float> input, py::array_t<float> kernel);
```

### Python Docstrings
```python
def conv2d(image, kernel):
    """
    Apply 2D convolution to an image.

    Args:
        image: Input image array (H, W) or (H, W, C)
        kernel: Convolution kernel (K, K)

    Returns:
        Convolved image array with same shape as input
    """
    pass
```

## Common Pitfalls

### Don't Over-Optimize
- Start with Python, optimize later
- Profile before optimizing
- Only optimize when it matters

### Don't Ignore Error Handling
- Always validate inputs
- Handle edge cases
- Provide meaningful error messages

### Don't Skip Testing
- Test both implementations
- Test edge cases
- Test performance

## Pro Tips

- **Start simple** - Get it working first, optimize later
- **Use both implementations** - Python for debugging, C++ for performance
- **Profile everything** - Measure before optimizing
- **Document as you go** - Don't leave it for later
- **Test early and often** - Catch issues before they become problems

## Next Steps

- Try the [Simple Tutorial](simple-tutorial.md) for hands-on practice
- Check [Testing](testing.md) for robust testing strategies
- Explore [Resources](resources.md) for advanced techniques
