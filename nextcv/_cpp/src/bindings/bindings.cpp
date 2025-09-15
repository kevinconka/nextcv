#include <Eigen/Core>
#include <cstdint>
#include <cstring>
#include <pybind11/buffer_info.h>
#include <pybind11/detail/common.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <stdexcept>
#include <vector>

#include "../core/hello.hpp"
#include "../image/invert.hpp"
#include "../linalg/matvec.hpp"
#include "../postprocessing/nms.hpp"

namespace py = pybind11;

namespace {

auto invert(const py::array_t<std::uint8_t>& input) -> py::array_t<std::uint8_t> {
    // Get buffer info from numpy array
    py::buffer_info buf_info = input.request();

    // Ensure array is C-contiguous for efficient processing
    if ((input.flags() & py::array::c_style) == 0) {
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

    // Core submodule
    auto core = module.def_submodule("core", "Core utilities");
    core.def("hello", &nextcv::core::hello, "Return a greeting from NextCV C++");

    // Image processing submodule
    auto image = module.def_submodule("image", "Image processing utilities");
    image.def("invert", &invert, "Invert n-dimensional array of 8-bit pixels, preserving shape");

    // Post-processing submodule
    auto postprocessing = module.def_submodule("postprocessing", "Post-processing utilities");
    postprocessing.def("nms", &nextcv::postprocessing::nms, py::arg("bboxes"), py::arg("scores"),
                       py::arg("threshold") = nextcv::postprocessing::default_nms_threshold,
                       "Apply Non-Maximum Suppression to bounding boxes (numpy arrays)");

    // Linear algebra submodule
    auto linalg = module.def_submodule("linalg", "Linear algebra utilities");

    // Accepts np.float32 arrays; returns np.float32 vector.
    linalg.def(
        "matvec",
        [](const Eigen::Ref<const Eigen::MatrixXf>& matrix,
           const Eigen::Ref<const Eigen::VectorXf>& vector) -> Eigen::VectorXf {
            return nextcv::linalg::matvec(matrix, vector);
        },
        py::arg("matrix"), py::arg("vector"),
        R"doc(Multiply matrix (MxN) by vector (N) → y (M). Uses Eigen.)doc");
}
