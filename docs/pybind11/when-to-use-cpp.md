# When to Use C++

Before you touch C++, ask yourself: **do I really need it?** C++ adds complexity, so use it only when it makes a meaningful impact.

!!! tip "The TL;DR"
    Only use C++ when you have a real performance bottleneck that can't be solved with existing Python tools.

## 🧠 The Decision Tree

=== "Question 1: Existing Solutions?"
    **Does a good Python library already exist?**
    ✅ Yes → Use it, don't reinvent the wheel.
    ❌ No → Continue to Question 2.

=== "Question 2: Performance Critical?"
    **Is this operation actually slow in Python?**
    ❌ No → Stick with Python (premature optimization ≠ productivity).
    ✅ Yes → Continue to Question 3.

=== "Question 3: Real Bottleneck?"
    **Is it a *real* production bottleneck?**
    ❌ No → Python is fine (users won't notice).
    ✅ Yes → Continue to Question 4.

=== "Question 4: C++ Advantage?"
    **Would C++ optimizations (SIMD, memory layout) make a big difference?**
    ❌ No → Try [NumPy](https://numpy.org/) or [Numba](https://numba.pydata.org/) first.
    ✅ Yes → 🚀 Write it in C++.

## ✅ Good Use Cases

!!! example "Real-World Examples"

    === "Non-Maximum Suppression (NMS)"
        - **Why:** Tight inner loops over many bounding boxes → Python too slow.
        - **Evidence:** [NMS benchmarks](https://github.com/ultralytics/yolov5/issues/5793) show 5–10× speedups with C++.
        - **Typical Use:** Object detection post-processing.

    === "Hungarian Algorithm"
        - **Why:** Matching problem grows O(n³), so Python overhead hurts fast.
        - **Evidence:** [SciPy's linear_sum_assignment](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html) is implemented in C for this reason.
        - **Typical Use:** Tracking and object assignment.

    === "Low-Level Hardware Access"
        - **Why:** Direct hardware control needs low-level access that Python can't provide.
        - **Evidence:** Libraries like WiringPi and pigpio are C-based for reliable timing.
        - **Typical Use:** IMU sensors, GPIO control, I2C/SPI communication.

## 🚩 Common Pitfalls

!!! danger "Watch Out For These"
    | Pitfall | Description | Better Approach |
    |---------|-------------|-----------------|
    | 🏃‍♂️ **"C++ is faster!"** | Assuming C++ automatically means better performance | - Profile with cProfile first<br>- Get concrete performance numbers<br>- Document real bottlenecks |
    | 🔧 **Reinventing the Wheel** | Writing C++ code for solved problems | - Check SciPy/NumPy first<br>- Use battle-tested implementations<br>- Focus on actual gaps |

## ✅ Final Checklist

!!! note "Before You Start"
    Use this checklist before diving into C++:

    - [ ] No good Python library exists
    - [ ] Profiling shows a clear bottleneck
    - [ ] Production workload hits this bottleneck
    - [ ] C++ will give meaningful gains
    - [ ] Team can maintain the C++ code

    If you check all boxes — go for it. Otherwise, stay in Python land. 🐍
