#include "invert.hpp"
#include "../core/types.hpp"
#include <algorithm>
#include <iterator>
#include <limits>

namespace nextcv::image {

auto invert(const core::PixelVector& pixels) -> core::PixelVector {
    core::PixelVector out;
    out.reserve(pixels.size());

    std::transform(pixels.begin(), pixels.end(), std::back_inserter(out),
                   [](core::Pixel pixel) -> core::Pixel {
                       return static_cast<core::Pixel>(std::numeric_limits<core::Pixel>::max() -
                                                       pixel);
                   });

    return out;
}

} // namespace nextcv::image
