# NextCV Repository Structure

This document describes the scalable structure implemented for the NextCV computer vision library.

## Overview

NextCV follows a modular architecture with clear separation between C++ core functionality and Python bindings. The structure is designed to be easily extensible for future features.

## Directory Structure

```
nextcv/
├── src/                          # C++ source code
│   ├── core/                     # Core utilities and base functionality
│   │   ├── hello.hpp/cpp         # Basic greeting functionality
│   │   ├── types.hpp             # Common type definitions
│   │   └── utils.hpp/cpp         # Utility functions
│   ├── image/                    # Image processing modules
│   │   ├── operations/           # Basic image operations
│   │   │   ├── invert.hpp/cpp    # Pixel inversion
│   │   │   └── threshold.hpp/cpp # Binary thresholding
│   │   ├── io/                   # Image I/O (future)
│   │   └── transform/            # Geometric transformations (future)
│   ├── features/                 # Feature detection and matching
│   │   ├── detection/            # Feature detection (future)
│   │   └── matching/             # Feature matching (future)
│   └── bindings/                 # Python bindings
│       └── bindings.cpp          # pybind11 bindings
├── nextcv/                       # Python package
│   ├── __init__.py               # Main package interface
│   ├── core/                     # Core Python utilities
│   │   ├── __init__.py
│   │   └── utils.py              # Python utility functions
│   ├── image/                    # Image processing Python interface
│   │   ├── __init__.py
│   │   └── operations.py         # Image operations
│   ├── features/                 # Feature detection Python interface
│   │   └── __init__.py
│   └── _internal/                # Internal C++ bindings
│       └── nextcv_py.pyi         # Type stubs
├── examples/                     # Usage examples
│   ├── cpp_example.cpp           # C++ usage example
│   └── python_example.py         # Python usage example
└── tests/                        # Test suite
    └── test_hello.py
```

## C++ Architecture

### Namespace Structure

```cpp
namespace nextcv {
    namespace core {
        // Core utilities, types, and base functionality
    }
    
    namespace image {
        namespace operations {
            // Image processing operations
        }
        namespace io {
            // Image I/O operations
        }
        namespace transform {
            // Geometric transformations
        }
    }
    
    namespace features {
        namespace detection {
            // Feature detection algorithms
        }
        namespace matching {
            // Feature matching algorithms
        }
    }
}
```

### Library Organization

- **nextcv_core**: Core utilities, types, and base functionality
- **nextcv_image**: Image processing operations (depends on nextcv_core)
- **nextcv_features**: Feature detection and matching (future, depends on nextcv_core)

## Python Architecture

### Package Structure

The Python package follows a modular design with clear separation of concerns:

- **nextcv.core**: Core utilities and version information
- **nextcv.image**: Image processing functionality
- **nextcv.features**: Feature detection and matching (future)
- **nextcv._internal**: Internal C++ bindings (not for direct use)

### Import Patterns

```python
# Main interface
import nextcv
nextcv.hello()
nextcv.invert(image)
nextcv.threshold(image, 128)

# Module-specific imports
from nextcv.core import get_version
from nextcv.image import invert, threshold
```

## Benefits of This Structure

### Scalability
- **Modular Design**: Each module can be developed independently
- **Clear Dependencies**: Dependencies are explicit and manageable
- **Namespace Organization**: Prevents naming conflicts and provides clear API boundaries

### Maintainability
- **Separation of Concerns**: C++ core, Python interface, and bindings are clearly separated
- **Consistent Patterns**: Similar functionality is organized consistently
- **Future-Ready**: Structure supports easy addition of new modules

### Extensibility
- **Easy to Add Features**: New functionality can be added to appropriate modules
- **Plugin Architecture**: New modules can be added without affecting existing code
- **API Consistency**: New functions follow established patterns

## Adding New Functionality

### C++ Side
1. Create appropriate header/source files in the relevant module directory
2. Add files to CMakeLists.txt
3. Update bindings if Python interface is needed
4. Add to appropriate namespace

### Python Side
1. Create new module files in the appropriate package directory
2. Update __init__.py files to export new functionality
3. Add type stubs if needed
4. Update examples and tests

## Future Expansion Areas

The current structure is designed to easily accommodate:

- **Image I/O**: Reading/writing various image formats
- **Geometric Transformations**: Resize, rotate, warp operations
- **Feature Detection**: Corner detection, blob detection, etc.
- **Feature Matching**: Template matching, feature descriptors
- **Machine Learning**: Integration with ML frameworks
- **Video Processing**: Video I/O and processing
- **GPU Acceleration**: CUDA/OpenCL support

This structure provides a solid foundation for building a comprehensive computer vision library while maintaining clean, maintainable code.