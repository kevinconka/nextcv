# NextCV Examples

Quick examples showing how to use NextCV for computer vision tasks.

## 📦 Core Module

```python
import nextcv as cvx

# Hello functions
print(cvx.core.hello_cpp())     # "Hello from C++!"
print(cvx.core.hello_python())  # "Hello from Python!"
```

## 🖼️ Image Module

```python
import numpy as np
import nextcv as cvx

# Image inversion
image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
inverted = cvx.image.invert(image)
print(f"Shape: {image.shape} -> {inverted.shape}")
```

## 🎯 Postprocessing Module

```python
import numpy as np
import nextcv as cvx

# Non-Maximum Suppression
boxes = np.array([[10, 10, 50, 50], [20, 20, 60, 60]], dtype=np.float32)
scores = np.array([0.9, 0.8], dtype=np.float32)

filtered = cvx.postprocessing.nms(boxes, scores, threshold=0.5)
print(f"Kept {len(filtered)} out of {len(boxes)} boxes")
```

---

<div align="center">

**Ready to build something amazing?** 🚀

[Get Started](getting-started.md) • [View API](reference/) • [Contribute](pybind11-guide.md)

</div>
