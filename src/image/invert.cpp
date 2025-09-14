#include "invert.hpp"
#include "../core/utils.hpp"

namespace nextcv {
namespace image {

core::PixelVector invert(const core::PixelVector& pixels) {
    core::PixelVector out;
    out.reserve(pixels.size());
    for (core::Pixel p : pixels) {
        out.push_back(static_cast<core::Pixel>(255 - p));
    }
    return out;
}

core::PixelVector invert(const core::PixelVector& pixels, const core::ImageSize& size) {
    core::validate_array_contiguity(pixels, size);
    return invert(pixels);
}

} // namespace image
} // namespace nextcv
