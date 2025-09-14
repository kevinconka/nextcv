#include "invert.hpp"
#include "../core/utils.hpp"

namespace nextcv {
namespace image {

core::PixelVector invert(const core::PixelVector& pixels) {
    constexpr core::Pixel MAX_PIXEL_VALUE = std::numeric_limits<core::Pixel>::max();
    core::PixelVector out;
    out.reserve(pixels.size());

    std::transform(pixels.begin(), pixels.end(), std::back_inserter(out),
                   [](core::Pixel p) { return static_cast<core::Pixel>(MAX_PIXEL_VALUE - p); });

    return out;
}

core::PixelVector invert(const core::PixelVector& pixels, const core::ImageSize& size) {
    core::validate_array_contiguity(pixels, size);
    return invert(pixels);
}

} // namespace image
} // namespace nextcv
