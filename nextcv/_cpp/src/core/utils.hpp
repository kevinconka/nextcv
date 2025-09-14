#pragma once

#include "types.hpp"
#include <stdexcept>

namespace nextcv {
namespace core {

/**
 * @brief Validate that the pixel array size matches the expected image dimensions
 * @param pixels The pixel array to validate
 * @param size Expected image dimensions
 * @throws std::invalid_argument if the array size doesn't match expected dimensions
 */
inline void validate_array_contiguity(const PixelVector& pixels, const ImageSize& size) {
    if (pixels.size() != size.total_pixels()) {
        throw std::invalid_argument("Pixel array size (" + std::to_string(pixels.size()) +
                                    ") doesn't match expected dimensions (" +
                                    std::to_string(size.width) + "x" + std::to_string(size.height) +
                                    "x" + std::to_string(size.channels) + " = " +
                                    std::to_string(size.total_pixels()) + " pixels)");
    }
}

} // namespace core
} // namespace nextcv
