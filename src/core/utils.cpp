#include "utils.hpp"
#include <sstream>

namespace nextcv {

std::string get_version() {
    return "0.1.0";
}

std::string get_build_info() {
    std::ostringstream oss;
    oss << "NextCV " << get_version() << " - Computer Vision Library";
    return oss.str();
}

bool is_valid_image_data(const PixelVector& data, const ImageSize& size) {
    return data.size() == size.total_pixels();
}

void validate_array_contiguity(const PixelVector& data, const ImageSize& size) {
    if (!is_valid_image_data(data, size)) {
        throw std::invalid_argument("Array data does not match expected size");
    }
}

} // namespace nextcv