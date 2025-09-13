#include "invert.hpp"
#include "../../core/utils.hpp"

namespace nextcv {
namespace image {
namespace operations {

PixelVector invert(const PixelVector& pixels) {
    PixelVector out;
    out.reserve(pixels.size());
    for (Pixel p : pixels) {
        out.push_back(static_cast<Pixel>(255 - p));
    }
    return out;
}

PixelVector invert(const PixelVector& pixels, const core::ImageSize& size) {
    core::validate_array_contiguity(pixels, size);
    return invert(pixels);
}

} // namespace operations
} // namespace image
} // namespace nextcv