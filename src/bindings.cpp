#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include "hello.hpp"
#include "invert.hpp"

namespace py = pybind11;

namespace {

py::array_t<std::uint8_t> invert(const py::array_t<std::uint8_t>& input) {
    // Get buffer info from numpy array
    py::buffer_info buf_info = input.request();

    // Check if the array is contiguous and 1D
    if (buf_info.ndim != 1) {
        throw std::runtime_error("Input array must be 1-dimensional");
    }

    // Convert to std::vector
    std::vector<std::uint8_t> pixels(static_cast<std::uint8_t*>(buf_info.ptr),
                                     static_cast<std::uint8_t*>(buf_info.ptr) + buf_info.size);

    // Apply inversion
    auto inverted = nextcv::invert(pixels);

    // Create output numpy array
    py::array_t<std::uint8_t> result(buf_info.size);
    py::buffer_info result_buf = result.request();
    std::memcpy(result_buf.ptr, inverted.data(), inverted.size() * sizeof(std::uint8_t));

    return result;
}

} // namespace

PYBIND11_MODULE(nextcv_py, m) {
    m.doc() = "NextCV pybind11 bindings";

    m.def("hello", &nextcv::hello, "Return a greeting from NextCV C++");
    m.def("invert", &invert, "Invert 8-bit pixels provided as numpy array, returns numpy array");
}
