<div align="center">

# NextCV

</div>

<div align="center">

**A modern computer vision library that bridges the gap between C++ performance and Python simplicity**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://en.cppreference.com/w/cpp/17)
[![Build Status](https://github.com/kevinconka/nextcv/workflows/CI/badge.svg)](https://github.com/kevinconka/nextcv/actions)

</div>

---

<div align="center">

## 🚀 What is NextCV?

</div>

NextCV is a **modern, minimal computer vision library** that combines the raw performance of C++ with the ease of use that Python developers love. Built from the ground up with contemporary tooling, it offers a clean API for both languages while maintaining the speed and efficiency that computer vision applications demand.

Think of it as **OpenCV reimagined** for the modern development workflow—with better packaging, cleaner APIs, and tooling that just works.

### ✨ Key Features

- **🚀 High Performance**: C++ core with Python bindings via pybind11
- **📦 Modern Packaging**: Built with scikit-build-core and managed with uv
- **🐍 Python-First**: Seamless NumPy integration and intuitive APIs
- **⚡ C++ Ready**: Header-only design with CMake integration
- **🔧 Developer Friendly**: Modern tooling, comprehensive testing, and clear documentation
- **📊 Cross-Platform**: Works on Windows, macOS, and Linux

---

<div align="center">

## 🛠️ Installation

</div>

### Python (Recommended)

```bash
# Using uv (recommended)
uv add nextcv

# Or with pip
pip install nextcv

# Or install directly from source
pip install git+https://github.com/kevinconka/nextcv.git
```

### C++

```cmake
# In your CMakeLists.txt
find_package(NextCV REQUIRED)
target_link_libraries(your_target PRIVATE NextCV::nextcv)
```

---

<div align="center">

## 🎯 Quick Start

</div>

### Python Example

```python
import nextcv
import numpy as np

# Simple hello world
print(nextcv.hello())

# Pixel inversion with NumPy arrays
data = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
inverted = nextcv.invert(data)
print(f"Original:  {data}")
print(f"Inverted:  {inverted}")
# Output: Original:  [  0  64 128 192 255]
#         Inverted:  [255 191 127  63   0]
```

### C++ Example

```cpp
#include "nextcv/invert.hpp"
#include <iostream>
#include <vector>

int main() {
    std::vector<uint8_t> pixels{0, 64, 128, 192, 255};
    auto inverted = nextcv::invert(pixels);

    for (auto pixel : inverted) {
        std::cout << static_cast<int>(pixel) << " ";
    }
    // Output: 255 191 127 63 0
}
```

---

<div align="center">

## 🏗️ Building from Source

</div>

### Prerequisites

- **Python 3.8+**
- **C++17 compatible compiler** (GCC 7+, Clang 5+, MSVC 2019+)
- **CMake 3.20+**
- **uv** (recommended) or pip

### Development Setup

```bash
# Clone the repository
git clone https://github.com/kevinconka/nextcv.git
cd nextcv

# Install pre-commit hooks (recommended)
uvx pre-commit install

# Python development
uv sync
uv run pytest
uv build

# C++ development
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
cmake --build build
./build/examples/cpp_example
```

### Running Examples

```bash
# Python example
uv run python examples/python_example.py

# C++ example
./build/examples/cpp_example
```

---

<div align="center">

## 🔧 Code Quality & Pre-commit

</div>

This project uses [pre-commit](https://pre-commit.com/) to ensure code quality and consistency. Pre-commit hooks automatically run checks and fixes on your code before each commit.

### Setup Pre-commit

```bash
# Install the git hook scripts
uvx pre-commit install

# (Optional) Run against all files
uvx pre-commit run --all-files
```

### What Pre-commit Does

The configured hooks will automatically:
- **Format code** with Ruff and clang-format
- **Remove unused imports** with pycln
- **Check for security issues** with gitleaks
- **Validate YAML/JSON** files
- **Remove trailing whitespace** and fix line endings
- **Check for large files** and case conflicts
- **Ensure test files** follow naming conventions

### Manual Usage

```bash
# Run all hooks on staged files
uvx pre-commit run

# Run specific hook
uvx pre-commit run ruff

# Update hook versions
uvx pre-commit autoupdate
```

---

<div align="center">

## 🧪 Testing

</div>

```bash
# Run Python tests
uv run pytest tests/ -v

# Run C++ tests
cmake -B build -DNEXTCV_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build
```

---

## 🤝 Contributing

We'd love your help making NextCV better! Whether you're fixing bugs, adding features, or improving documentation, every contribution matters.

### How to Contribute

1. **Fork the repository** and create a feature branch
2. **Write tests** for your changes (we love good test coverage!)
3. **Run the test suite** to ensure everything works
4. **Submit a pull request** with a clear description of your changes

### What We're Looking For

- 🐛 **Bug fixes** and performance improvements
- ✨ **New algorithms** and computer vision features
- 📖 **Documentation** improvements and examples
- 🧪 **Tests** that make us go "wow, we didn't think of that"
- 🎨 **Code quality** improvements and refactoring

### Development Guidelines

- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and well-described

---

<div align="center">

## 📋 Project Status

</div>

**Current Version**: 0.0.1 (Experimental)

This is an experimental project in active development. The API may change between versions as we refine the design and add new features.

### Roadmap

- [ ] Core image processing functions
- [ ] Feature detection algorithms
- [ ] Machine learning integration
- [ ] GPU acceleration support
- [ ] Extended platform support

---

<div align="center">

## 🏛️ Architecture

</div>

NextCV is built with a clean, modular architecture:

```
┌─────────────────┐    ┌─────────────────┐
│   Python API    │    │    C++ API      │
│   (pybind11)    │    │   (Headers)     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌──────────▼───────────┐
          │    C++ Core Library  │
          │   (High Performance) │
          └──────────────────────┘
```

- **C++ Core**: High-performance algorithms and data structures
- **Python Bindings**: Seamless integration with NumPy and Python ecosystem
- **Modern Build System**: CMake + scikit-build-core for reliable cross-platform builds

---

<div align="center">

## 📄 License

</div>

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

## 🙏 Acknowledgments

</div>

- Built with [pybind11](https://github.com/pybind/pybind11) for Python-C++ interop
- Powered by [scikit-build-core](https://github.com/scikit-build/scikit-build-core) for modern Python packaging
- Managed with [uv](https://github.com/astral-sh/uv) for fast dependency resolution
- Inspired by the computer vision community and open source projects

---

<div align="center">

**Ready to build the future of computer vision?** 🚀

[Get Started](#-quick-start) • [View Examples](examples/) • [Contribute](#-contributing) • [Report Issues](https://github.com/kevinconka/nextcv/issues)

</div>
