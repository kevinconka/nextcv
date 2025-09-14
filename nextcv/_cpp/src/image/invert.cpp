#include "invert.hpp"
#include "../core/utils.hpp"
#include "/Users/kevinserrano/GitHub/kevinconka/nextcv/nextcv/_cpp/src/core/types.hpp"
#include <algorithm>
#include <iterator>
#include <limits>

namespace nextcv::image {

auto invert(const core::PixelVector& pixels) -> core::PixelVector {
    core::PixelVector out;
    out.reserve(pixels.size());

    std::transform(pixels.begin(), pixels.end(), std::back_inserter(out),
                   [](core::Pixel p) -> core::Pixel {
                       return static_cast<core::Pixel>(std::numeric_limits<core::Pixel>::max() - p);
                   });

    return out;
}

auto invert(const core::PixelVector& pixels, const core::ImageSize& size) -> core::PixelVector {
    core::validateArrayContiguity(pixels, size);
    return invert(pixels);
}

} // namespace nextcv::image
