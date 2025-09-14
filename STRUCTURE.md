# NextCV Repository Structure

NextCV follows NumPy's organizational pattern with C++ source files under `nextcv/_cpp/src/` and Python modules at the package level.

## Directory Structure

```
nextcv/
├── nextcv/                       # Python package
│   ├── _cpp/                     # C++ source code and bindings
│   │   ├── src/                  # C++ source files
│   │   │   ├── core/             # Core functionality
│   │   │   ├── image/            # Image processing
│   │   │   ├── postprocessing/   # Post-processing
│   │   │   └── bindings/         # Python bindings
│   │   └── nextcv_py.pyi         # Type stubs
│   ├── core/                     # Python core module
│   ├── image/                    # Python image module
│   └── postprocessing/           # Python postprocessing module
├── examples/                     # Usage examples
└── tests/                        # Test suite
```

## API Design

```python
import nextcv as cvx

# C++ wrapped functions (high performance)
cvx.image.invert(image)
cvx.postprocessing.nms_cpp(boxes, 0.5)
cvx.core.hello_cpp()

# Python implementations (debugging/fallback)
cvx.postprocessing.nms_np(boxes, 0.5)
cvx.core.hello_python()
```

## Key Principles

1. **NumPy-style organization**: C++ files under `nextcv/_cpp/src/`
2. **Mixed implementations**: C++ for performance, Python for debugging
3. **Automatic CMake discovery**: No manual file listing required
4. **Clear naming**: `function_cpp()` vs `function_python()`

## Adding New Functions

**C++ Side:**
1. Add files to `nextcv/_cpp/src/module/`
2. Use namespace: `namespace nextcv { namespace module { ... } }`
3. Update bindings if needed
4. Run `make tidy` to check code quality

**Python Side:**
1. Add to `nextcv/module/__init__.py`
2. Create both implementations: `function_cpp()` and `function_python()`
3. Export in `__all__` list
4. Run `uv run ruff check` to check code quality
