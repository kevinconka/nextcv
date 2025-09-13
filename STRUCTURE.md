# NextCV Repository Structure

This document describes the mixed C++/Python structure implemented for the NextCV computer vision library, providing both high-performance C++ implementations and pure Python fallbacks in the same modules.

## Overview

NextCV follows a mixed architecture where each functional module can contain both C++ and Python implementations, allowing users to choose the best implementation for their needs. The structure provides clear organization while remaining intuitive and flexible.

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
│   ├── core/                     # Mixed C++/Python core module
│   │   └── __init__.py           # hello, hello_python, get_version
│   ├── image/                    # Mixed C++/Python image processing
│   │   └── __init__.py           # invert, invert_python, threshold
│   ├── postprocessing/           # Mixed C++/Python post-processing
│   │   └── __init__.py           # nms, fast_nms, nms_python
│   ├── utils/                    # Pure Python utilities
│   │   └── __init__.py           # load_image, save_image, draw_boxes
│   ├── features/                 # Pure Python features (for now)
│   │   └── __init__.py           # detect_corners, detect_corners_python
│   └── _internal/                # Internal C++ bindings
│       └── nextcv_py.pyi         # Type stubs
├── examples/                     # Usage examples
│   ├── cpp_example.cpp           # C++ usage example
│   ├── python_example.py         # Python usage example
│   └── mixed_api_example.py      # Mixed API usage example
└── tests/                        # Test suite
    └── test_hello.py
```

## Mixed API Architecture

### Functional Modules with Mixed Implementations

```python
# Mixed modules - C++ as default, Python as fallback
from nextcv.image import invert, invert_python
from nextcv.postprocessing import nms, fast_nms, nms_python
from nextcv.core import hello, hello_python

# Pure Python modules
from nextcv.utils import load_image, save_image, draw_boxes
from nextcv.features import detect_corners, detect_corners_python
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
        PixelVector invert(const PixelVector& pixels);
        PixelVector threshold(const PixelVector& pixels, Pixel threshold);
    }
    
    namespace postprocessing {
        // Post-processing functions
        std::vector<BoundingBox> nms(const std::vector<BoundingBox>& boxes, float threshold);
    }
}
```

### Module Organization

- **nextcv.core**: Mixed C++/Python core functionality
  - `hello()` - Default implementation (C++ if available, Python fallback)
  - `hello_python()` - Always Python implementation
  - `get_version()` - Version information
- **nextcv.image**: Mixed C++/Python image processing
  - `invert()` - Default implementation (C++ if available, Python fallback)
  - `invert_python()` - Always Python implementation
  - `threshold()` - Binary thresholding
- **nextcv.postprocessing**: Mixed C++/Python post-processing
  - `nms()` - Default implementation (C++ if available, Python fallback)
  - `fast_nms()` - Alias for C++ implementation
  - `nms_python()` - Always Python implementation
- **nextcv.utils**: Pure Python utilities
  - `load_image()`, `save_image()` - Image I/O
  - `resize_image()`, `normalize_image()` - Image utilities
  - `draw_boxes()` - Visualization
- **nextcv.features**: Pure Python features (for now)
  - `detect_corners()` - Corner detection

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

### 1. **Mixed Implementations** (Best of Both Worlds)
- C++ as default for performance-critical functions
- Python fallback when C++ not available
- Clear naming: `function_name()` vs `function_name_python()`
- Easy to choose the right implementation

### 2. **Automatic CMake Discovery**
- Uses `GLOB_RECURSE` to automatically find all `.cpp` files
- No need to manually update CMakeLists.txt when adding files
- Modern CMake syntax with proper target linking

### 3. **Functional Module Organization**
- **core/**: Core functionality (mixed C++/Python)
- **image/**: Image processing (mixed C++/Python)
- **postprocessing/**: Post-processing (mixed C++/Python)
- **utils/**: Utilities (pure Python)
- **features/**: Feature detection (pure Python for now)

### 4. **Intuitive Naming Convention**
- `function_name()` - Default implementation (C++ if available, Python fallback)
- `function_name_python()` - Always Python implementation
- `fast_function_name()` - Alias for C++ implementation
- Clear distinction between implementations

## Benefits of This Mixed Structure

### **Ease of Use**
- **Intuitive Organization**: Functions grouped by functionality
- **Flexible Choice**: Choose C++ for performance, Python for debugging
- **Clear Implementation**: Function name indicates implementation type
- **Fallback Support**: Python implementations work when C++ isn't available

### **Easy Maintenance**
- **Automatic CMake**: No manual file listing required
- **Self-Documenting**: Structure clearly shows module organization
- **Future-Proof**: Easy to add new modules without restructuring

### **Industry Best Practices**
- **Familiar Pattern**: Mixed implementations are common in scientific libraries
- **Proven Design**: Provides flexibility without complexity
- **Industry Standard**: Follows established mixed-language library patterns

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

| Module | Default Function | Python Function | C++ Alias | Description |
|--------|------------------|-----------------|-----------|-------------|
| core | `hello()` | `hello_python()` | - | Greeting message |
| image | `invert()` | `invert_python()` | - | Image inversion |
| postprocessing | `nms()` | `nms_python()` | `fast_nms()` | Non-Maximum Suppression |
| utils | `load_image()` | - | - | Image I/O (Python-only) |
| features | `detect_corners()` | `detect_corners_python()` | - | Corner detection |

## Future Expansion

The mixed structure easily accommodates:

- **New Image Operations**: Add to `src/image/` → `nextcv.image.new_function()`
- **Feature Detection**: Add to `src/features/` → `nextcv.features.new_function()`
- **Machine Learning**: Add `src/ml/` → `nextcv.ml.new_function()`
- **Video Processing**: Add `src/video/` → `nextcv.video.new_function()`
- **GPU Support**: Add `src/gpu/` → `nextcv.gpu.new_function()`

Each new module follows the same pattern:
- Mixed implementations: `function()` and `function_python()`
- Automatic CMake discovery
- Clear naming convention
- Fallback support

This structure provides the perfect balance of performance and flexibility, making it easy to use and extend while providing clear implementation choices.