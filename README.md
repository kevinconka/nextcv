<div align="center">

# NextCV

**Python's ease, C++'s speed. Finally.**

</div>

<div align="center">

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://en.cppreference.com/w/cpp/17)
[![Build Status](https://github.com/kevinconka/nextcv/workflows/CI/badge.svg)](https://github.com/kevinconka/nextcv/actions)

</div>

---

<div align="center">

**For those who want the full story, [read the docs](https://kevinconka.github.io/nextcv/). For everyone else, here's the gist.**

</div>

---

## What is this?

It's a computer vision library. You write Python, because you're not a masochist. But when your code inevitably becomes a bottleneck, you need speed. That's where we come in.

We use C++ for the heavy lifting, so you don't have to. It's not magic, it's just good engineering.

**The philosophy is simple:**

> Write Python. When it's slow, we make it fast.

---

## Does it actually work?

Yes. Here's a Non-Maximum Suppression (NMS) benchmark. We pitted our C++ implementation against a standard NumPy version.

```python
import time
import numpy as np
from nextcv.postprocessing import nms_cpp, nms_np

# A respectable amount of data
N = 10000
rng = np.random.default_rng(42)
bboxes = rng.uniform(0, 100, (N, 4)).astype(np.float32)
scores = rng.uniform(0.1, 1, N).astype(np.float32)

# Time the C++ version
start_time = time.perf_counter()
result_cpp = nms_cpp(bboxes, scores, 0.5)
cpp_time = time.perf_counter() - start_time

# Time the NumPy version
start_time = time.perf_counter()
result_np = nms_np(bboxes, scores, 0.5)
np_time = time.perf_counter() - start_time

print("NMS Timing Comparison:")
print(f"   Dataset: {len(bboxes)} bounding boxes")
print(f"   nms_cpp(): {len(result_cpp)} boxes kept in {cpp_time * 1000:.2f}ms")
print(f"   nms_np(): {len(result_np)} boxes kept in {np_time * 1000:.2f}ms")
```

**The numbers don't lie.** The C++ version is significantly faster.

---

## How do I use it?

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install libeigen3-dev cmake

# MacOS
brew install eigen cmake
```

### Installation

Get it, obviously. Use `uv` if you know what's good for you.

```bash
# traditional pip
pip install git+https://github.com/kevinconka/nextcv.git

# uv
uv add git+https://github.com/kevinconka/nextcv.git
```

### Check it's working

```bash
uv run python -c "import nextcv; print(nextcv.__version__)"
```

### Building from source

This project uses a dual-configuration approach to support both modern development and legacy compatibility:

- **Modern builds** (Python 3.9+): Uses `scikit-build-core` with `pyproject.toml`
- **Legacy builds** (Python 3.6+): Uses `scikit-build` with `pyproject.legacy.toml` + `setup.py`

**For development (Python 3.9+):**

```bash
pip install -e .
```

**For Jetson boards (Python 3.6+):**

```bash
# Copy legacy config and build
cp pyproject.legacy.toml pyproject.toml
pip install -e .
```

The CI/CD automatically tests both configurations across Python 3.6, 3.8, and 3.9.

### Contributing

If you think you can make this better, feel free. Just don't break anything.

1.  **Fork it.**
2.  **Create a branch.** (`git checkout -b my-brilliant-idea`)
3.  **Install Python tools.**

    ```bash
    # Install uv (if you don't have it)
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

4.  **Install C++ tools.**

    ```bash
    # macOS
    brew install clang-format llvm
    # Add LLVM to PATH (add to ~/.zshrc or ~/.bash_profile)
    echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.zshrc

    # Ubuntu/Debian
    sudo apt-get install clang-format clang-tidy
    ```

5.  **Set up the environment.**
    ```bash
    uv sync
    uvx pre-commit install
    ```
6.  **Write code.** And tests. Don't forget the tests.
7.  **Run the checks.**
    ```bash
    uv run pytest
    uvx pre-commit run --all-files
    ```
8.  **Open a pull request.** Make it a good one.

---

<div align="center">

**That's it. Now you know.**

</div>
