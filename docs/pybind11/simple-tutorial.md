# Simple PyBind11 Tutorial

Let's build something basic - a simple function that adds two numbers. This is the "Hello World" of PyBind11.

## What We're Building

A C++ function that adds two integers, bound to Python. Nothing fancy, just the fundamentals.

## Step 1: C++ Function

Create a simple header:

```cpp
// nextcv/_cpp/src/core/add.hpp
#pragma once

int add(int a, int b);
```

Implement it:

```cpp
// nextcv/_cpp/src/core/add.cpp
#include "add.hpp"

int add(int a, int b) {
    return a + b;
}
```

## Step 2: Python Binding

Add to your bindings file:

```cpp
// nextcv/_cpp/src/bindings/bindings.cpp
#include <pybind11/pybind11.h>
#include "../core/add.hpp"

PYBIND11_MODULE(nextcv_py, module) {
    module.def("add", &add, "Add two integers");
}
```

## Step 3: Use It

```python
import nextcv as cvx

result = cvx.add(5, 3)  # Returns 8
print(result)
```

## That's It!

You've just created your first PyBind11 binding. The C++ function is now available in Python with zero overhead.

## Next Steps

- Try binding a function that takes NumPy arrays
- Add error handling
- Explore more complex data types

**Remember**: Start simple, then add complexity as needed.
