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

## What is NextCV?

**Fast computer vision in Python.** C++ performance with Python simplicity.

- **C++ speed** + **Python ease** via pybind11
- **Modern tooling** (uv, scikit-build-core)
- **Cross-platform** (macOS, Linux)
- **CI/CD** (GitHub Actions)

---

## 🛠️ Installation

```bash
# Using uv (recommended)
uv add nextcv

# Or with pip
pip install git+https://github.com/kevinconka/nextcv.git
```

### C++ (CMake)

```cmake
find_package(NextCV REQUIRED)
target_link_libraries(your_target PRIVATE NextCV::nextcv)
```

---

## 🎯 Quick Start

**Install and run:**
```bash
uv add nextcv
uv run python -c "import nextcv; print(nextcv.hello_cpp())"
uv run python -c "import nextcv; print(nextcv.hello_python())"
```

**Performance demo:**
```python
import timeit
import numpy as np
from nextcv.postprocessing import nms_cpp, nms_np

N = 1_000
rng = np.random.default_rng(42)
bboxes = rng.uniform(0, 100, (N, 4)).astype(np.float32)
scores = rng.uniform(0.1, 1, N).astype(np.float32)

t_cpp = timeit.timeit("nms_cpp(bboxes, scores, 0.5)", globals=globals(), number=100)
t_np = timeit.timeit("nms_np(bboxes, scores, 0.5)", globals=globals(), number=100)

print(f"nms_cpp: {t_cpp:.2f} ms/call")
print(f"nms_np:  {t_np:.2f} ms/call")

>>> nms_cpp: 0.17 ms/call
>>> nms_np:  2.22 ms/call
```

**Or run the full example:**
```bash
uv run python examples/python_example.py
```

---

## 🏗️ Building from Source

**Prerequisites**: Python 3.8+, C++17 compiler, CMake 3.20+, uv

```bash
# Clone and setup
git clone https://github.com/kevinconka/nextcv.git
cd nextcv

# Install pre-commit hooks
uvx pre-commit install

# Development
uv sync && uv run pytest
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON && cmake --build build
```

---

## 🧪 Development & Testing

```bash
# Run tests
uv run pytest tests/ -v

# Code quality (pre-commit)
uvx pre-commit install
uvx pre-commit run --all-files
```

---

## 🤝 Contributing

1. Fork the repository and create a feature branch
2. Write tests for your changes
3. Submit a pull request

### Development Tools Setup

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get install -y clang-format clang-tidy
```

**macOS**
```bash
brew install llvm

# Add LLVM to PATH (auto-detects shell)
if [ -n "$ZSH_VERSION" ]; then
  echo 'export PATH="$(brew --prefix llvm)/bin:$PATH"' >> ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
  echo 'export PATH="$(brew --prefix llvm)/bin:$PATH"' >> ~/.bashrc
fi

# Reload shell
source ~/.zshrc    # or ~/.bashrc
```

### Development Workflow

**Pre-commit Setup**
```bash
uvx pre-commit install
uvx pre-commit run --all-files
```

**Python Development**
```bash
uv sync
uv run pytest tests/ -v
uv run ruff check .
uv run ruff format .
```

**C++ Development**
```bash
cmake -B build -DNEXTCV_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build
clang-format -i src/**/*.{cpp,hpp}
clang-tidy src/**/*.cpp
```

We welcome bug fixes, new features, documentation improvements, and code quality enhancements.

---

## 🏛️ Architecture

NextCV is built with a clean, modular architecture:
- **C++ Core**: High-performance algorithms and data structures
- **Python Bindings**: Seamless integration with NumPy and Python ecosystem
- **Modern Build System**: CMake + scikit-build-core for reliable cross-platform builds

---

<div align="center">

## 📄 License

</div>

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with [pybind11](https://github.com/pybind/pybind11), [scikit-build-core](https://github.com/scikit-build/scikit-build-core), and [uv](https://github.com/astral-sh/uv).

---

<div align="center">

**Ready to build the future of computer vision?** 🚀

[Get Started](#-quick-start) • [View Examples](examples/) • [Contribute](#-contributing) • [Report Issues](https://github.com/kevinconka/nextcv/issues)

</div>
