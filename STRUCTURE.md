# NextCV Repository Structure

This document describes the simplified structure implemented for the NextCV computer vision library, providing only essential functions with both C++ and Python implementations.

## Overview

NextCV follows a simplified architecture with only essential functions, using the `cvx` import pattern for clear module.function() syntax. The structure provides both high-performance C++ implementations and pure Python fallbacks where needed.

## Directory Structure

```
nextcv/
├── src/                          # C++ source code
│   ├── core/                     # Core functionality
│   │   ├── hello.hpp/cpp         # Basic greeting functionality
│   │   └── types.hpp             # Common type definitions
│   ├── image/                    # Image processing
│   │   └── invert.hpp/cpp        # Pixel inversion
│   ├── postprocessing/           # Post-processing operations
│   │   └── nms.hpp/cpp           # Non-Maximum Suppression
│   └── bindings/                 # Python bindings
│       └── bindings.cpp          # pybind11 bindings
├── nextcv/                       # Python package
│   ├── __init__.py               # Main package interface
│   ├── core/                     # Core functionality
│   │   └── __init__.py           # hello, hello_python
│   ├── image/                    # Image processing
│   │   └── __init__.py           # invert, invert_python
│   ├── postprocessing/           # Post-processing
│   │   └── __init__.py           # nms (Python), nms_fast (C++)
│   └── _internal/                # Internal C++ bindings
│       └── nextcv_py.pyi         # Type stubs
├── examples/                     # Usage examples
│   ├── cpp_example.cpp           # C++ usage example
│   ├── python_example.py         # Python usage example
│   └── simplified_example.py     # Simplified API example
└── tests/                        # Test suite
    └── test_hello.py
```

## Simplified API Architecture

### Essential Functions Only

```python
import nextcv as cvx

# C++ wrapped functions
cvx.image.invert(image)
cvx.postprocessing.nms_fast(boxes, 0.5)
cvx.core.hello()

# Python implementations
cvx.postprocessing.nms(boxes, 0.5)
cvx.image.invert_python(image)
cvx.core.hello_python()
```

### C++ Namespace Structure

```cpp
namespace nextcv {
    namespace core {
        // Core functions
        std::string hello();
        std::string get_version();
    }

    namespace image {
        // Image processing functions
        PixelVector invert(const PixelVector& pixels);    }

    namespace postprocessing {
        // Post-processing functions
        std::vector<BoundingBox> nms(const std::vector<BoundingBox>& boxes, float threshold);
    }
}
```

### Module Organization

- **cvx.core**: Core functionality
  - `hello()` - C++ wrapped
  - `hello_python()` - Python implementation
- **cvx.image**: Image processing
  - `invert()` - C++ wrapped
  - `invert_python()` - Python implementation
- **cvx.postprocessing**: Post-processing
  - `nms()` - Python implementation (default)
  - `nms_fast()` - C++ wrapped

### Modern CMake with Automatic File Discovery

```cmake
# Automatically discover all .cpp files in each module
file(GLOB_RECURSE CORE_SOURCES "core/*.cpp")
file(GLOB_RECURSE IMAGE_SOURCES "image/*.cpp")
file(GLOB_RECURSE POSTPROC_SOURCES "postprocessing/*.cpp")
file(GLOB_RECURSE FEATURES_SOURCES "features/*.cpp")

# No need to manually update CMakeLists.txt when adding new files!
```

## Python Architecture

### Mixed Module Structure

The Python package uses functional modules with mixed C++/Python implementations:

```python
# Mixed modules - C++ as default, Python as fallback
from nextcv.image import invert, invert_python
from nextcv.postprocessing import nms, fast_nms, nms_python
from nextcv.core import hello, hello_python

# Pure Python modules
from nextcv.utils import load_image, save_image, draw_boxes
from nextcv.features import detect_corners, detect_corners_python
```

### Import Patterns

```python
# Performance-critical code (uses C++ if available)
from nextcv.image import invert
result = invert(image)  # C++ if available, Python fallback

# Debugging or when C++ not available
from nextcv.image import invert_python
result = invert_python(image)  # Always Python

# Explicit C++ usage
from nextcv.postprocessing import fast_nms
result = fast_nms(boxes, 0.5)  # C++ implementation

# Utilities (always Python)
from nextcv.utils import load_image, draw_boxes
image = load_image("input.jpg")
result = draw_boxes(image, boxes)
```

## Key Design Principles

### 1. **Essential Functions Only**
- Only core functionality: hello, invert, nms
- No unnecessary utilities or I/O code
- Clean and simple structure

### 2. **Clear Import Pattern**
- `import nextcv as cvx` for familiar syntax
- `cvx.module.function()` for clear organization
- Easy to understand and use

### 3. **Mixed Implementations**
- C++ for performance: `invert()`, `nms_fast()`, `hello()`
- Python for debugging: `invert_python()`, `nms()`, `hello_python()`
- Clear naming convention

### 4. **Automatic CMake Discovery**
- Uses `GLOB_RECURSE` to automatically find all `.cpp` files
- No need to manually update CMakeLists.txt when adding files
- Modern CMake syntax with proper target linking

## Benefits of This Simplified Structure

### **Ease of Use**
- **Essential Functions Only**: No unnecessary complexity
- **Clear Import Pattern**: `cvx.module.function()` syntax
- **Mixed Implementations**: C++ for performance, Python for debugging
- **Simple Structure**: Easy to understand and extend

### **Easy Maintenance**
- **Automatic CMake**: No manual file listing required
- **Clean Code**: Only essential functionality
- **Simple PR**: Minimal changes for easy review

### **Industry Best Practices**
- **Familiar Pattern**: `cvx` import like OpenCV
- **Proven Design**: Simple and effective
- **Industry Standard**: Follows established computer vision library patterns

## Adding New Functionality

### C++ Side
1. **Add files to appropriate module directory** (e.g., `src/image/new_function.hpp/cpp`)
2. **CMake automatically discovers them** - no manual updates needed!
3. **Use two-level namespace**: `namespace nextcv { namespace image { ... } }`
4. **Update bindings** if Python interface is needed

### Python Side
1. **Add to appropriate module** (e.g., `nextcv/image/__init__.py`)
2. **Create both implementations**: `new_function()` and `new_function_python()`
3. **Set default**: `new_function = _new_function_cpp if available else _new_function_python`
4. **Export both**: Add to `__all__` list

## Implementation Examples

| Module | C++ Function | Python Function | Description |
|--------|--------------|-----------------|-------------|
| core | `hello()` | `hello_python()` | Greeting message |
| image | `invert()` | `invert_python()` | Image inversion |
| postprocessing | `nms_fast()` | `nms()` | Non-Maximum Suppression |

## Future Expansion

The simplified structure easily accommodates:

- **New Image Operations**: Add to `src/image/` → `cvx.image.new_function()`
- **Feature Detection**: Add to `src/features/` → `cvx.features.new_function()`
- **Machine Learning**: Add `src/ml/` → `cvx.ml.new_function()`
- **Video Processing**: Add `src/video/` → `cvx.video.new_function()`
- **GPU Support**: Add `src/gpu/` → `cvx.gpu.new_function()`

Each new module follows the same pattern:
- C++ and Python implementations
- Automatic CMake discovery
- Clear `cvx.module.function()` syntax
- Simple and clean structure

This structure provides the perfect balance of simplicity and functionality, making it easy to use and extend while keeping the PR clean and simple.
