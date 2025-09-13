#include "threshold.hpp"
#include "../core/utils.hpp"

namespace nextcv {
namespace image {

PixelVector threshold(const PixelVector& pixels, Pixel threshold, Pixel max_value) {
    PixelVector out;
    out.reserve(pixels.size());
    for (Pixel p : pixels) {
        out.push_back(p > threshold ? max_value : 0);
    }
    return out;
}

PixelVector threshold(const PixelVector& pixels, const core::ImageSize& size, 
                     Pixel threshold, Pixel max_value) {
    core::validate_array_contiguity(pixels, size);
    return threshold(pixels, threshold, max_value);
}

} // namespace image
} // namespace nextcv