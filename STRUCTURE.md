# NextCV Repository Structure

This document describes the simplified, scalable structure implemented for the NextCV computer vision library, inspired by OpenCV's design philosophy.

## Overview

NextCV follows a simplified modular architecture with a single namespace (like OpenCV's `cv` namespace) and automatic CMake file discovery. The structure is designed to be easily extensible without namespace confusion or manual CMake maintenance.

## Directory Structure

```
nextcv/
├── src/                          # C++ source code
│   ├── core/                     # Core utilities and base functionality
│   │   ├── hello.hpp/cpp         # Basic greeting functionality
│   │   ├── types.hpp             # Common type definitions
│   │   └── utils.hpp/cpp         # Utility functions
│   ├── imgproc/                  # Image processing (like OpenCV's imgproc)
│   │   ├── invert.hpp/cpp        # Pixel inversion
│   │   └── threshold.hpp/cpp     # Binary thresholding
│   ├── features/                 # Feature detection and matching (future)
│   │   └── (empty, ready for expansion)
│   └── bindings/                 # Python bindings
│       └── bindings.cpp          # pybind11 bindings
├── nextcv/                       # Python package
│   ├── __init__.py               # Main package interface
│   └── _internal/                # Internal C++ bindings
│       └── nextcv_py.pyi         # Type stubs
├── examples/                     # Usage examples
│   ├── cpp_example.cpp           # C++ usage example
│   └── python_example.py         # Python usage example
└── tests/                        # Test suite
    └── test_hello.py
```

## C++ Architecture

### Simplified Namespace Structure

```cpp
namespace nextcv {
    // All functions directly in nextcv namespace
    // Like OpenCV's cv namespace
    
    // Core functions
    std::string hello();
    std::string get_version();
    
    // Image processing functions
    PixelVector invert(const PixelVector& pixels);
    PixelVector threshold(const PixelVector& pixels, Pixel threshold);
}
```

### Library Organization

- **nextcv_core**: Core utilities, types, and base functionality
- **nextcv_imgproc**: Image processing operations (depends on nextcv_core)
- **nextcv_features**: Feature detection and matching (future, depends on nextcv_core)

### Modern CMake with Automatic File Discovery

```cmake
# Automatically discover all .cpp files in each module
file(GLOB_RECURSE CORE_SOURCES "core/*.cpp")
file(GLOB_RECURSE IMGPROC_SOURCES "imgproc/*.cpp")
file(GLOB_RECURSE FEATURES_SOURCES "features/*.cpp")

# No need to manually update CMakeLists.txt when adding new files!
```

## Python Architecture

### Simplified Package Structure

The Python package uses a flat structure with all functions directly accessible:

```python
import nextcv

# All functions directly available
nextcv.hello()
nextcv.invert(image)
nextcv.threshold(image, 128)
nextcv.get_version()
```

### Import Patterns

```python
# Simple, direct imports (like OpenCV)
import nextcv
result = nextcv.invert(image)

# Or import specific functions
from nextcv import invert, threshold
result = invert(image)
```

## Key Design Principles

### 1. **Single Namespace** (Like OpenCV)
- All C++ functions in `nextcv` namespace
- No deep nesting like `nextcv::image::operations::invert()`
- Simple: `nextcv::invert()`

### 2. **Automatic CMake Discovery**
- Uses `GLOB_RECURSE` to automatically find all `.cpp` files
- No need to manually update CMakeLists.txt when adding files
- Modern CMake syntax with proper target linking

### 3. **Module-Based Organization**
- **core/**: Basic utilities and types
- **imgproc/**: Image processing (like OpenCV's imgproc module)
- **features/**: Feature detection (like OpenCV's features2d module)

### 4. **Simple Python API**
- All functions directly accessible from `nextcv` package
- No complex module hierarchy
- Clean, intuitive interface

## Benefits of This Simplified Structure

### **Ease of Use**
- **Simple API**: `nextcv::invert()` instead of `nextcv::image::operations::invert()`
- **No Namespace Confusion**: Single namespace like OpenCV
- **Intuitive**: Functions are where you expect them

### **Easy Maintenance**
- **Automatic CMake**: No manual file listing required
- **Self-Documenting**: Structure clearly shows module organization
- **Future-Proof**: Easy to add new modules without restructuring

### **OpenCV Compatibility**
- **Familiar Pattern**: Developers familiar with OpenCV will feel at home
- **Proven Design**: OpenCV's single namespace approach has worked for decades
- **Industry Standard**: Follows established computer vision library patterns

## Adding New Functionality

### C++ Side
1. **Add files to appropriate module directory** (e.g., `src/imgproc/new_function.hpp/cpp`)
2. **CMake automatically discovers them** - no manual updates needed!
3. **Use simple namespace**: `namespace nextcv { ... }`
4. **Update bindings** if Python interface is needed

### Python Side
1. **Add to bindings.cpp** for new C++ functions
2. **Update __init__.py** to export new functions
3. **Functions automatically available** as `nextcv.new_function()`

## Comparison with OpenCV

| Aspect | OpenCV | NextCV |
|--------|--------|--------|
| Namespace | `cv::` | `nextcv::` |
| Image Processing | `cv::imgproc` module | `src/imgproc/` directory |
| Core Functions | `cv::core` module | `src/core/` directory |
| Python API | `cv.invert()` | `nextcv.invert()` |
| CMake | Manual file listing | Automatic discovery |

## Future Expansion

The simplified structure easily accommodates:

- **New Image Operations**: Add to `src/imgproc/`
- **Feature Detection**: Add to `src/features/`
- **Machine Learning**: Add `src/ml/` module
- **Video Processing**: Add `src/video/` module
- **GPU Support**: Add `src/gpu/` module

Each new module follows the same simple pattern:
- Single `nextcv` namespace
- Automatic CMake discovery
- Direct Python API access

This structure provides the perfect balance of simplicity and scalability, making it easy to use and extend without the complexity of deep namespace hierarchies.