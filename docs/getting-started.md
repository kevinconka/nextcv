# Getting Started with NextCV

Welcome to NextCV! This guide will get you up and running with our modern computer vision library in no time.

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- C++17 compiler (GCC, Clang, or MSVC)
- CMake 3.20 or higher

### Quick Install

```bash
# Using uv (recommended)
uv add nextcv

# Or with pip
pip install git+https://github.com/kevinconka/nextcv.git
```

### From Source

```bash
# Clone the repository
git clone https://github.com/kevinconka/nextcv.git
cd nextcv

# Install dependencies
uv sync

# Build and install
uv run pip install -e .
```

## 🎯 Your First NextCV Program

Let's start with something simple:

```python
import nextcv as cvx

# Say hello to NextCV
print(cvx.hello_cpp())  # "Hello from NextCV (C++)"
print(cvx.hello_python())  # "Hello from NextCV (Python)"
```

## 🖼️ Image Processing

NextCV excels at image processing with C++ performance:

```python
import numpy as np
import nextcv as cvx

# Create a sample image
image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
print(f"Original image shape: {image.shape}")

# Invert the image (C++ implementation)
inverted = cvx.image.invert(image)
print(f"Inverted image shape: {inverted.shape}")

# The result maintains the same shape and dtype
assert inverted.shape == image.shape
assert inverted.dtype == image.dtype
```

## 📦 Post-Processing

NextCV includes efficient post-processing algorithms:

```python
import numpy as np
import nextcv as cvx

# Create some bounding boxes and scores
boxes = np.array([
    [10, 10, 50, 50],   # x1, y1, x2, y2
    [20, 20, 60, 60],
    [15, 15, 55, 55],   # Overlapping with first box
], dtype=np.float32)

scores = np.array([0.9, 0.8, 0.7], dtype=np.float32)

# Apply Non-Maximum Suppression
filtered_boxes = cvx.postprocessing.nms_cpp(boxes, scores, threshold=0.5)
print(f"Original boxes: {len(boxes)}")
print(f"Filtered boxes: {len(filtered_boxes)}")
```

## ⚡ Performance Comparison

Let's see the performance difference between C++ and Python implementations:

```python
import timeit
import numpy as np
import nextcv as cvx

# Create test data
N = 1000
rng = np.random.default_rng(42)
boxes = rng.uniform(0, 100, (N, 4)).astype(np.float32)
scores = rng.uniform(0.1, 1, N).astype(np.float32)

# Time C++ implementation
t_cpp = timeit.timeit(
    "cvx.postprocessing.nms_cpp(boxes, scores, 0.5)", 
    globals=globals(), 
    number=100
)

# Time Python implementation  
t_py = timeit.timeit(
    "cvx.postprocessing.nms_np(boxes, scores, 0.5)", 
    globals=globals(), 
    number=100
)

print(f"C++ NMS: {t_cpp:.2f} ms/call")
print(f"Python NMS: {t_py:.2f} ms/call")
print(f"Speedup: {t_py/t_cpp:.1f}x")
```

## 🧪 Running Examples

NextCV comes with example scripts:

```bash
# Run the Python example
uv run python examples/python_example.py

# Build and run C++ example (if building from source)
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
cmake --build build
./build/examples/cpp_example
```

## 🔧 Development Setup

If you want to contribute to NextCV:

```bash
# Install development dependencies
uv sync --all-extras

# Install pre-commit hooks
uvx pre-commit install

# Run tests
uv run pytest tests/ -v

# Check code quality
uv run ruff check .
uv run ruff format .
```

## 🆘 Troubleshooting

### Common Issues

**Import Error**: Make sure you have the required dependencies:
```bash
uv add numpy opencv-python
```

**Build Error**: Ensure you have a C++17 compiler and CMake installed:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake

# macOS
brew install cmake
```

**Performance Issues**: Make sure you're using the C++ implementations (functions ending with `_cpp`) for better performance.

## 🎓 Next Steps

Now that you're up and running:

1. **[Explore the API Reference](reference/)** - See all available functions
2. **[Learn PyBind11 Development](pybind11-guide.md)** - Add your own C++ functions
3. **[Check out Examples](examples/)** - More complex use cases

Happy coding! 🚀