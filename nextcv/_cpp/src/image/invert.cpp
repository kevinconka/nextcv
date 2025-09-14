#include "invert.hpp"
#include "../core/utils.hpp"
#include <algorithm>
#include <limits>

namespace nextcv {
namespace image {

core::PixelVector invert(const core::PixelVector& pixels) {
    core::PixelVector out;
    out.reserve(pixels.size());

    std::transform(pixels.begin(), pixels.end(), std::back_inserter(out), [](core::Pixel p) {
        return static_cast<core::Pixel>(std::numeric_limits<core::Pixel>::max() - p);
    });

    return out;
}

core::PixelVector invert(const core::PixelVector& pixels, const core::ImageSize& size) {
    core::validate_array_contiguity(pixels, size);
    return invert(pixels);
}

} // namespace image
} // namespace nextcv
