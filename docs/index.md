# What is NextCV?

**Fast computer vision in Python.** C++ performance with Python simplicity.

NextCV is like OpenCV but with modern tooling. It's a minimal, experimental CV library built with:

- **C++ speed** + **Python ease** via pybind11
- **Modern tooling** (uv, scikit-build-core)
- **Cross-platform** (macOS, Linux)
- **CI/CD** (GitHub Actions)

## 🚀 Quick Start

```bash
# Using uv (recommended)
uv add git+https://github.com/kevinconka/nextcv.git

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

## ☕️ Buy Me a Coffee

Primpting AI agents is hard! Coffees are needed when AI agents derail so much I actually have to write code.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kevinconka)
