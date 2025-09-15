# NextCV Documentation

<div align="center">

**A modern computer vision library that bridges the gap between C++ performance and Python simplicity**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://en.cppreference.com/w/cpp/17)

</div>

---

## What is NextCV?

**Fast computer vision in Python.** C++ performance with Python simplicity.

NextCV is like OpenCV but with modern tooling. It's a minimal, experimental CV library built with:

- **C++ speed** + **Python ease** via pybind11
- **Modern tooling** (uv, scikit-build-core)
- **Cross-platform** (macOS, Linux)
- **CI/CD** (GitHub Actions)

## 🚀 Quick Start

```bash
# Using uv (recommended)
uv add nextcv

# Or with pip
pip install git+https://github.com/kevinconka/nextcv.git
```

```python
import nextcv as cvx

# C++ wrapped functions (high performance)
print(cvx.hello_cpp())  # "Hello from NextCV (C++)"

# Image processing
import numpy as np
image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
inverted = cvx.image.invert(image)

# Post-processing
boxes = np.array([[10, 10, 50, 50], [20, 20, 60, 60]], dtype=np.float32)
scores = np.array([0.9, 0.8], dtype=np.float32)
filtered_boxes = cvx.postprocessing.nms_cpp(boxes, scores, 0.5)
```

## 🏗️ Architecture

NextCV follows a clean, modular architecture:

- **C++ Core**: High-performance algorithms and data structures
- **Python Bindings**: Seamless integration with NumPy and Python ecosystem  
- **Modern Build System**: CMake + scikit-build-core for reliable cross-platform builds

## 📚 Documentation

- **[Getting Started](getting-started.md)** - Installation and basic usage
- **[PyBind11 Guide](pybind11-guide.md)** - Learn how to create C++ wrapped code
- **[API Reference](reference/)** - Complete API documentation
- **[Examples](examples/)** - Code examples and tutorials

## 🤝 Contributing

We welcome contributions! Check out our [PyBind11 Guide](pybind11-guide.md) to learn how to add new C++ functions with Python bindings.

---

<div align="center">

**Ready to build the future of computer vision?** 🚀

[Get Started](getting-started.md) • [View Examples](examples/) • [Contribute](pybind11-guide.md)

</div>