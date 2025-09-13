# NextCV Repository Structure

This document describes the two-level namespace structure implemented for the NextCV computer vision library, providing clear organization without excessive complexity.

## Overview

NextCV follows a modular architecture with two-level namespaces (e.g., `nextcv::image::invert()`) and automatic CMake file discovery. The structure provides clear organization while remaining simple and extensible.

## Directory Structure

```
nextcv/
├── src/                          # C++ source code
│   ├── core/                     # Core utilities and base functionality
│   │   ├── hello.hpp/cpp         # Basic greeting functionality
│   │   ├── types.hpp             # Common type definitions
│   │   └── utils.hpp/cpp         # Utility functions
│   ├── image/                    # Image processing
│   │   ├── invert.hpp/cpp        # Pixel inversion
│   │   └── threshold.hpp/cpp     # Binary thresholding
│   ├── postprocessing/           # Post-processing operations
│   │   └── nms.hpp/cpp           # Non-Maximum Suppression
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

### Two-Level Namespace Structure

```cpp
namespace nextcv {
    namespace core {
        // Core functions
        std::string hello();
        std::string get_version();
    }
    
    namespace image {
        // Image processing functions
        PixelVector invert(const PixelVector& pixels);
        PixelVector threshold(const PixelVector& pixels, Pixel threshold);
    }
    
    namespace postprocessing {
        // Post-processing functions
        std::vector<BoundingBox> nms(const std::vector<BoundingBox>& boxes, float threshold);
    }
}
```

### Library Organization

- **nextcv_core**: Core utilities, types, and base functionality
- **nextcv_image**: Image processing operations (depends on nextcv_core)
- **nextcv_postprocessing**: Post-processing operations (depends on nextcv_core)
- **nextcv_features**: Feature detection and matching (future, depends on nextcv_core)

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

### Simplified Package Structure

The Python package uses a flat structure with all functions directly accessible:

```python
import nextcv

# All functions directly available
nextcv.hello()
nextcv.invert(image)
nextcv.threshold(image, 128)
nextcv.nms(boxes, 0.5)
nextcv.get_version()
```

### Import Patterns

```python
# Simple, direct imports (like OpenCV)
import nextcv
result = nextcv.invert(image)
filtered_boxes = nextcv.nms(boxes, 0.5)

# Or import specific functions
from nextcv import invert, threshold, nms
result = invert(image)
filtered = nms(boxes, 0.5)
```

## Key Design Principles

### 1. **Two-Level Namespaces** (Perfect Balance)
- Clear organization: `nextcv::image::invert()`
- Logical grouping: `nextcv::postprocessing::nms()`
- Not too deep: `nextcv::core::get_version()`
- Easy to understand and extend

### 2. **Automatic CMake Discovery**
- Uses `GLOB_RECURSE` to automatically find all `.cpp` files
- No need to manually update CMakeLists.txt when adding files
- Modern CMake syntax with proper target linking

### 3. **Module-Based Organization**
- **core/**: Basic utilities and types
- **image/**: Image processing operations
- **postprocessing/**: Post-processing operations (NMS, etc.)
- **features/**: Feature detection and matching

### 4. **Simple Python API**
- All functions directly accessible from `nextcv` package
- No complex module hierarchy
- Clean, intuitive interface

## Benefits of This Two-Level Structure

### **Ease of Use**
- **Clear Organization**: `nextcv::image::invert()` is intuitive and organized
- **Logical Grouping**: Related functions are grouped together
- **Not Too Deep**: Two levels provide clarity without complexity
- **Intuitive**: Functions are where you expect them

### **Easy Maintenance**
- **Automatic CMake**: No manual file listing required
- **Self-Documenting**: Structure clearly shows module organization
- **Future-Proof**: Easy to add new modules without restructuring

### **Industry Best Practices**
- **Familiar Pattern**: Two-level namespaces are common in C++ libraries
- **Proven Design**: Provides organization without complexity
- **Industry Standard**: Follows established C++ library patterns

## Adding New Functionality

### C++ Side
1. **Add files to appropriate module directory** (e.g., `src/image/new_function.hpp/cpp`)
2. **CMake automatically discovers them** - no manual updates needed!
3. **Use two-level namespace**: `namespace nextcv { namespace image { ... } }`
4. **Update bindings** if Python interface is needed

### Python Side
1. **Add to bindings.cpp** for new C++ functions
2. **Update __init__.py** to export new functions
3. **Functions automatically available** as `nextcv.new_function()`

## Namespace Examples

| Function Category | C++ Namespace | Example Function |
|-------------------|---------------|------------------|
| Core utilities | `nextcv::core::` | `nextcv::core::get_version()` |
| Image processing | `nextcv::image::` | `nextcv::image::invert()` |
| Post-processing | `nextcv::postprocessing::` | `nextcv::postprocessing::nms()` |
| Features | `nextcv::features::` | `nextcv::features::detect_corners()` |

## Future Expansion

The two-level structure easily accommodates:

- **New Image Operations**: Add to `src/image/` → `nextcv::image::new_function()`
- **Feature Detection**: Add to `src/features/` → `nextcv::features::new_function()`
- **Machine Learning**: Add `src/ml/` → `nextcv::ml::new_function()`
- **Video Processing**: Add `src/video/` → `nextcv::video::new_function()`
- **GPU Support**: Add `src/gpu/` → `nextcv::gpu::new_function()`

Each new module follows the same pattern:
- Two-level namespace: `nextcv::module::function()`
- Automatic CMake discovery
- Direct Python API access

This structure provides the perfect balance of organization and simplicity, making it easy to use and extend without namespace confusion or excessive complexity.