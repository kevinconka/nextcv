# Getting Started

This guide will walk you through installing NextCV and running your first performance demo.

## 1. Prerequisites

=== "Linux"

    ```bash
    sudo apt-get install libeigen3-dev cmake
    ```

=== "macOS"

    ```bash
    brew install eigen cmake
    ```

## 2. Installation

=== "pip"

      ```bash
      pip install git+https://github.com/kevinconka/nextcv.git
      ```

=== "uv"

      ```bash
      uv add git+https://github.com/kevinconka/nextcv.git
      ```

## 3. Performance Demo

This example demonstrates the performance difference between the C++ and NumPy implementations of Non-Maximum Suppression (NMS).

```python
import time
import numpy as np
from nextcv.postprocessing import nms_cpp, nms_np

# Create a large dataset of bounding boxes
N = 10000
rng = np.random.default_rng(42)
bboxes = rng.uniform(0, 100, (N, 4)).astype(np.float32)
scores = rng.uniform(0.1, 1, N).astype(np.float32)

# Time C++ implementation
start_time = time.perf_counter()
result_cpp = nms_cpp(bboxes, scores, 0.5)
cpp_time = time.perf_counter() - start_time

# Time NumPy implementation
start_time = time.perf_counter()
result_np = nms_np(bboxes, scores, 0.5)
np_time = time.perf_counter() - start_time

print("Post-processing (NMS timing comparison):")
print(f"   Dataset: {len(bboxes)} bounding boxes")
print(f"   nms_cpp(): {len(result_cpp)} boxes kept in {cpp_time * 1000:.2f}ms")
print(f"   nms_np(): {len(result_np)} boxes kept in {np_time * 1000:.2f}ms")
```

**Output:**

```
Post-processing (NMS timing comparison):
   Dataset: 10000 bounding boxes
   nms_cpp(): 950 boxes kept in 25.93ms
   nms_np(): 949 boxes kept in 65.39ms
```

## 4. Next Steps

Now that you have NextCV installed, you can start exploring the API.

- **Explore the API:** Check out the [API Reference](../reference) for a full list of available functions.
- **Learn about our philosophy:** Read our guide on [When to Use C++](../pybind11/when-to-use-cpp.md) to understand our approach to performance.
