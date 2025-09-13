#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include "hello.hpp"
#include "invert.hpp"

namespace py = pybind11;

namespace {

py::bytes invert_bytes(const py::bytes& input) {
    // Extract bytes to std::string (holds raw bytes)
    std::string buffer = input;
    std::vector<std::uint8_t> pixels(buffer.begin(), buffer.end());
    auto inverted = nextcv::invert(pixels);
    return py::bytes(reinterpret_cast<const char*>(inverted.data()), inverted.size());
}

} // namespace

PYBIND11_MODULE(nextcv_py, m) {
    m.doc() = "NextCV pybind11 bindings";

    m.def("hello", &nextcv::hello, "Return a greeting from NextCV C++");
    m.def("invert", &invert_bytes, "Invert 8-bit pixels provided as bytes-like, returns bytes");
}
