#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>   // Eigen <-> NumPy conversions

#include "../core/hello.hpp"
#include "../image/invert.hpp"
#include "../postprocessing/nms.hpp"
#include "../linalg/matvec.hpp"

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
    auto inverted = nextcv::image::invert(pixels);

    // Create output numpy array with same shape as input
    py::array_t<std::uint8_t> result(buf_info.shape);
    py::buffer_info result_buf = result.request();
    std::memcpy(result_buf.ptr, inverted.data(), inverted.size() * sizeof(std::uint8_t));

    return result;
}

} // namespace

PYBIND11_MODULE(nextcv_py, module) {
    module.doc() = "NextCV pybind11 bindings";

    // Core functions
    module.def("hello", &nextcv::core::hello, "Return a greeting from NextCV C++");

    // Image processing functions
    module.def("invert", &invert, "Invert n-dimensional array of 8-bit pixels, preserving shape");

    module.def("nms", &nextcv::postprocessing::nms, py::arg("bboxes"), py::arg("scores"),
               py::arg("threshold") = 0.5f,
               "Apply Non-Maximum Suppression to bounding boxes (numpy arrays)");

    // Linear algebra submodule
    auto linalg = module.def_submodule("linalg", "Linear algebra utilities");

    // Accepts np.float32 arrays; returns np.float32 vector.
    linalg.def(
        "matvec",
        [](const Eigen::Ref<const Eigen::MatrixXf>& A,
           const Eigen::Ref<const Eigen::VectorXf>& x) {
          return nextcv::linalg::matvec(A, x);
        },
        py::arg("A"), py::arg("x"),
        R"doc(Multiply matrix A (M×N) by vector x (N) → y (M). Uses Eigen.)doc");
}
