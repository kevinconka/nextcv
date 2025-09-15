# PyBind11 Development Guide

So you want to add some C++ functions to NextCV? Buckle up, because we're about to make your Python code absolutely **blazing fast**! 🚀

This guide will walk you through creating C++ wrapped code using pybind11, following NextCV's architecture and best practices.

## 🏗️ NextCV Architecture Overview

NextCV follows a clean, modular structure:

```
nextcv/
├── _cpp/src/           # C++ source code
│   ├── core/           # Core functionality
│   ├── image/          # Image processing
│   ├── postprocessing/ # Post-processing algorithms
│   └── bindings/       # Python bindings
├── core/               # Python core module
├── image/              # Python image module
└── postprocessing/     # Python postprocessing module
```

**Key Principle**: Every C++ function gets both a C++ implementation AND a Python implementation for debugging/fallback.

## 🎯 Step-by-Step: Adding a New Function

Let's add a simple image blur function to demonstrate the process. We'll call it `gaussian_blur` because, well, that's what it does.

### Step 1: Create the C++ Header

First, let's create the header file:

```cpp
// nextcv/_cpp/src/image/gaussian_blur.hpp
#pragma once

#include <vector>
#include <cstdint>

namespace nextcv::image {

/**
 * @brief Apply Gaussian blur to a 1D array of pixels
 * @param pixels Input pixel array (flattened image)
 * @param width Image width
 * @param height Image height
 * @param channels Number of channels (1 for grayscale, 3 for RGB)
 * @param sigma Gaussian kernel standard deviation
 * @return Blurred pixel array
 */
auto gaussian_blur(
    const std::vector<std::uint8_t>& pixels,
    int width,
    int height,
    int channels,
    float sigma = 1.0f
) -> std::vector<std::uint8_t>;

} // namespace nextcv::image
```

### Step 2: Implement the C++ Function

Now the actual implementation:

```cpp
// nextcv/_cpp/src/image/gaussian_blur.cpp
#include "gaussian_blur.hpp"
#include <cmath>
#include <algorithm>

namespace nextcv::image {

auto gaussian_blur(
    const std::vector<std::uint8_t>& pixels,
    int width,
    int height,
    int channels,
    float sigma
) -> std::vector<std::uint8_t> {
    
    // Create output array
    std::vector<std::uint8_t> result(pixels.size());
    
    // Calculate kernel size (odd number, at least 3)
    int kernel_size = std::max(3, static_cast<int>(2 * std::ceil(2 * sigma) + 1));
    if (kernel_size % 2 == 0) kernel_size++;
    
    int half_kernel = kernel_size / 2;
    
    // Generate Gaussian kernel
    std::vector<float> kernel(kernel_size);
    float kernel_sum = 0.0f;
    
    for (int i = 0; i < kernel_size; ++i) {
        float x = i - half_kernel;
        kernel[i] = std::exp(-(x * x) / (2 * sigma * sigma));
        kernel_sum += kernel[i];
    }
    
    // Normalize kernel
    for (float& k : kernel) {
        k /= kernel_sum;
    }
    
    // Apply horizontal blur
    std::vector<std::uint8_t> temp(pixels.size());
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            for (int c = 0; c < channels; ++c) {
                float sum = 0.0f;
                for (int k = 0; k < kernel_size; ++k) {
                    int px = x + k - half_kernel;
                    px = std::clamp(px, 0, width - 1);
                    int idx = (y * width + px) * channels + c;
                    sum += pixels[idx] * kernel[k];
                }
                temp[(y * width + x) * channels + c] = 
                    static_cast<std::uint8_t>(std::round(sum));
            }
        }
    }
    
    // Apply vertical blur
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            for (int c = 0; c < channels; ++c) {
                float sum = 0.0f;
                for (int k = 0; k < kernel_size; ++k) {
                    int py = y + k - half_kernel;
                    py = std::clamp(py, 0, height - 1);
                    int idx = (py * width + x) * channels + c;
                    sum += temp[idx] * kernel[k];
                }
                result[(y * width + x) * channels + c] = 
                    static_cast<std::uint8_t>(std::round(sum));
            }
        }
    }
    
    return result;
}

} // namespace nextcv::image
```

### Step 3: Add Python Bindings

Update the bindings file:

```cpp
// nextcv/_cpp/src/bindings/bindings.cpp
// ... existing includes ...
#include "../image/gaussian_blur.hpp"

namespace py = pybind11;

namespace {

py::array_t<std::uint8_t> gaussian_blur(
    const py::array_t<std::uint8_t>& input,
    float sigma = 1.0f
) {
    // Get buffer info
    py::buffer_info buf_info = input.request();
    
    if (input.ndim() < 2) {
        throw std::runtime_error("Input must be at least 2D");
    }
    
    // Ensure C-contiguous
    if (!(input.flags() & py::array::c_style)) {
        throw std::runtime_error("Input array must be C-contiguous");
    }
    
    // Extract dimensions
    int height = input.shape(0);
    int width = input.shape(1);
    int channels = input.ndim() == 3 ? input.shape(2) : 1;
    
    // Convert to vector
    std::vector<std::uint8_t> pixels(
        static_cast<std::uint8_t*>(buf_info.ptr),
        static_cast<std::uint8_t*>(buf_info.ptr) + buf_info.size
    );
    
    // Apply blur
    auto blurred = nextcv::image::gaussian_blur(pixels, width, height, channels, sigma);
    
    // Create output array
    py::array_t<std::uint8_t> result(buf_info.shape);
    py::buffer_info result_buf = result.request();
    std::memcpy(result_buf.ptr, blurred.data(), blurred.size() * sizeof(std::uint8_t));
    
    return result;
}

} // namespace

PYBIND11_MODULE(nextcv_py, module) {
    // ... existing bindings ...
    
    // Add new binding
    module.def("gaussian_blur", &gaussian_blur, 
               py::arg("input"), py::arg("sigma") = 1.0f,
               "Apply Gaussian blur to an image array");
}
```

### Step 4: Create Python Implementation

Now let's create the Python fallback implementation:

```python
# nextcv/image/blur.py
"""Image blurring functions."""

import numpy as np
from typing import Union


def gaussian_blur_python(
    image: np.ndarray, 
    sigma: float = 1.0
) -> np.ndarray:
    """
    Apply Gaussian blur to an image (Python implementation).
    
    Args:
        image: Input image array
        sigma: Gaussian kernel standard deviation
        
    Returns:
        Blurred image array
    """
    from scipy import ndimage
    
    if image.ndim == 2:
        # Grayscale
        return ndimage.gaussian_filter(image, sigma=sigma)
    elif image.ndim == 3:
        # Color
        result = np.zeros_like(image)
        for c in range(image.shape[2]):
            result[:, :, c] = ndimage.gaussian_filter(image[:, :, c], sigma=sigma)
        return result
    else:
        raise ValueError("Image must be 2D or 3D")
```

### Step 5: Update Python Module

Update the image module's `__init__.py`:

```python
# nextcv/image/__init__.py
"""Image processing functions."""

from .ops import invert_cpp, invert_python
from .blur import gaussian_blur_python

# Import C++ functions
try:
    from .._cpp.nextcv_py import gaussian_blur as gaussian_blur_cpp
except ImportError:
    gaussian_blur_cpp = None

def gaussian_blur(image, sigma=1.0):
    """Apply Gaussian blur to an image."""
    if gaussian_blur_cpp is not None:
        return gaussian_blur_cpp(image, sigma)
    else:
        return gaussian_blur_python(image, sigma)

__all__ = [
    "invert_cpp", "invert_python", "invert",
    "gaussian_blur_cpp", "gaussian_blur_python", "gaussian_blur"
]
```

### Step 6: Update CMakeLists.txt

Add the new source file to the CMake build:

```cmake
# nextcv/_cpp/src/image/CMakeLists.txt
# ... existing files ...
set(SOURCES
    invert.cpp
    gaussian_blur.cpp  # Add this line
)

# ... rest of the file ...
```

## 🧪 Testing Your Function

Create a test to make sure everything works:

```python
# tests/image/test_blur.py
import numpy as np
import pytest
import nextcv as cvx

def test_gaussian_blur():
    # Create test image
    image = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
    
    # Test C++ implementation
    blurred_cpp = cvx.image.gaussian_blur_cpp(image, sigma=1.0)
    assert blurred_cpp.shape == image.shape
    assert blurred_cpp.dtype == image.dtype
    
    # Test Python implementation
    blurred_py = cvx.image.gaussian_blur_python(image, sigma=1.0)
    assert blurred_py.shape == image.shape
    assert blurred_py.dtype == image.dtype
    
    # Test wrapper function
    blurred = cvx.image.gaussian_blur(image, sigma=1.0)
    assert blurred.shape == image.shape

def test_gaussian_blur_grayscale():
    # Test grayscale image
    image = np.random.randint(0, 255, (50, 50), dtype=np.uint8)
    blurred = cvx.image.gaussian_blur(image, sigma=1.0)
    assert blurred.shape == image.shape
```

## 🚀 Performance Tips

### 1. Use NumPy Arrays Efficiently

```cpp
// Good: Check flags and use direct pointer access
if (!(input.flags() & py::array::c_style)) {
    throw std::runtime_error("Input array must be C-contiguous");
}
std::memcpy(result_buf.ptr, data.data(), data.size() * sizeof(T));
```

### 2. Minimize Python Object Creation

```cpp
// Good: Reuse buffers when possible
static thread_local std::vector<float> temp_buffer;
temp_buffer.resize(size);
```

### 3. Use Appropriate Data Types

```cpp
// Good: Use fixed-width integers for consistency
std::vector<std::uint8_t> pixels;
// Avoid: std::vector<int> for pixel data
```

## 🔧 Debugging Tips

### 1. Test Both Implementations

Always test both C++ and Python versions to ensure they produce the same results:

```python
# Compare implementations
result_cpp = cvx.image.gaussian_blur_cpp(image, sigma=1.0)
result_py = cvx.image.gaussian_blur_python(image, sigma=1.0)
np.testing.assert_allclose(result_cpp, result_py, rtol=1e-5)
```

### 2. Use Python Implementation for Debugging

When debugging, temporarily force the Python implementation:

```python
# Force Python implementation
cvx.image.gaussian_blur_cpp = None
result = cvx.image.gaussian_blur(image)  # Will use Python version
```

### 3. Check Memory Layout

```python
# Ensure arrays are C-contiguous
assert image.flags.c_contiguous, "Array must be C-contiguous"
```

## 📚 Best Practices

### 1. Naming Conventions

- C++ functions: `snake_case`
- Python functions: `snake_case` with `_cpp` and `_python` suffixes
- Wrapper functions: `snake_case` (no suffix)

### 2. Error Handling

```cpp
// Always validate inputs
if (input.ndim() < 2) {
    throw std::runtime_error("Input must be at least 2D");
}
```

### 3. Documentation

```cpp
/**
 * @brief Brief description
 * @param param1 Description of param1
 * @param param2 Description of param2
 * @return Description of return value
 */
```

### 4. Type Safety

```cpp
// Use strong typing
auto result = nextcv::image::gaussian_blur(pixels, width, height, channels, sigma);
// Not: auto result = gaussian_blur(pixels, w, h, c, s);
```

## 🎉 You're Ready!

Now you know how to add C++ functions to NextCV! The key is:

1. **C++ Implementation** - Fast, efficient algorithm
2. **Python Bindings** - Bridge between C++ and Python
3. **Python Fallback** - For debugging and compatibility
4. **Wrapper Function** - Smart choice between implementations
5. **Tests** - Ensure everything works correctly

Go forth and make some blazing fast computer vision code! 🔥

## 📖 Additional Resources

- [PyBind11 Documentation](https://pybind11.readthedocs.io/)
- [NumPy C API](https://numpy.org/doc/stable/reference/c-api/)
- [CMake Documentation](https://cmake.org/documentation/)
- [NextCV API Reference](reference/) - See existing implementations