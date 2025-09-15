# PyBind11 Basics

PyBind11 is a header-only library that exposes C++ code to Python. Think of it as a translator that handles type conversions, memory management, and NumPy integration.

## Core Concepts

### Module Definition

```cpp
PYBIND11_MODULE(module_name, module) {
    // Your bindings go here
}
```

### Function Binding

```cpp
// Simple function
module.def("function_name", &cpp_function, "Documentation");

// With arguments
module.def("function_name", &cpp_function,
           py::arg("arg1"), py::arg("arg2") = default_value,
           "Documentation");
```

### NumPy Array Handling

```cpp
py::array_t<float> my_function(py::array_t<float> input) {
    py::buffer_info buf_info = input.request();
    float* ptr = static_cast<float*>(buf_info.ptr);
    // Process data...
    return output;
}
```

## Essential Types

| C++ Type | Python Type | Notes |
|----------|-------------|-------|
| `int` | `int` | Automatic conversion |
| `float` | `float` | Automatic conversion |
| `std::vector<T>` | `list` | Automatic conversion |
| `py::array_t<T>` | `numpy.ndarray` | NumPy arrays |

## Common Patterns

### Input Validation

```cpp
if (input.ndim() != 2) {
    throw std::runtime_error("Input must be 2D");
}
```

### Memory Access

```cpp
py::buffer_info buf = input.request();
float* ptr = static_cast<float*>(buf.ptr);
```

### Return Arrays

```cpp
py::array_t<float> output({height, width});
py::buffer_info out_buf = output.request();
std::memcpy(out_buf.ptr, result.data(), size * sizeof(float));
return output;
```

## Pro Tips

- **Always validate inputs** - Check dimensions, types, and contiguity
- **Use C-contiguous arrays** - Much faster for processing
- **Handle exceptions properly** - They become Python exceptions
- **Document your functions** - PyBind11 uses the docstrings

## Next Steps

- Try the [Simple Tutorial](simple-tutorial.md) for hands-on practice
- Check [Best Practices](best-practices.md) for advanced techniques
- Explore [Testing](testing.md) for robust code
