#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include "../core/hello.hpp"
#include "../core/utils.hpp"
#include "../imgproc/invert.hpp"
#include "../imgproc/threshold.hpp"

namespace py = pybind11;

namespace {

py::array_t<std::uint8_t> invert(const py::array_t<std::uint8_t>& input) {
    // Get buffer info from numpy array
    py::buffer_info buf_info = input.request();

    // Ensure array is C-contiguous for efficient processing
    if (!(input.flags() & py::array::c_style)) {
        throw std::runtime_error("Input array must be C-contiguous");
    }

    // Convert to std::vector for processing (flattened view)
    std::vector<std::uint8_t> pixels(static_cast<std::uint8_t*>(buf_info.ptr),
                                     static_cast<std::uint8_t*>(buf_info.ptr) + buf_info.size);

    // Apply inversion
    auto inverted = nextcv::invert(pixels);

    // Create output numpy array with same shape as input
    py::array_t<std::uint8_t> result(buf_info.shape);
    py::buffer_info result_buf = result.request();
    std::memcpy(result_buf.ptr, inverted.data(), inverted.size() * sizeof(std::uint8_t));

    return result;
}

py::array_t<std::uint8_t> threshold(const py::array_t<std::uint8_t>& input, 
                                   std::uint8_t threshold, 
                                   std::uint8_t max_value = 255) {
    // Get buffer info from numpy array
    py::buffer_info buf_info = input.request();

    // Ensure array is C-contiguous for efficient processing
    if (!(input.flags() & py::array::c_style)) {
        throw std::runtime_error("Input array must be C-contiguous");
    }

    // Convert to std::vector for processing (flattened view)
    std::vector<std::uint8_t> pixels(static_cast<std::uint8_t*>(buf_info.ptr),
                                     static_cast<std::uint8_t*>(buf_info.ptr) + buf_info.size);

    // Apply threshold
    auto thresholded = nextcv::threshold(pixels, threshold, max_value);

    // Create output numpy array with same shape as input
    py::array_t<std::uint8_t> result(buf_info.shape);
    py::buffer_info result_buf = result.request();
    std::memcpy(result_buf.ptr, thresholded.data(), thresholded.size() * sizeof(std::uint8_t));

    return result;
}

} // namespace

PYBIND11_MODULE(nextcv_py, m) {
    m.doc() = "NextCV pybind11 bindings";

    // Core functions
    m.def("hello", &nextcv::hello, "Return a greeting from NextCV C++");
    m.def("get_version", &nextcv::get_version, "Get NextCV version");
    m.def("get_build_info", &nextcv::get_build_info, "Get build information");

    // Image processing functions
    m.def("invert", &invert, "Invert n-dimensional array of 8-bit pixels, preserving shape");
    m.def("threshold", &threshold, 
          py::arg("input"), 
          py::arg("threshold"), 
          py::arg("max_value") = 255,
          "Apply binary threshold to n-dimensional array of 8-bit pixels");
}