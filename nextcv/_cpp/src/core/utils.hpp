#pragma once

#include "types.hpp"
#include <stdexcept>

namespace nextcv::core {

/**
 * @brief Validate that the pixel array size matches the expected image dimensions
 * @param pixels The pixel array to validate
 * @param size Expected image dimensions
 * @throws std::invalid_argument if the array size doesn't match expected dimensions
 */
inline void validateArrayContiguity(const PixelVector& pixels, const ImageSize& size) {
    if (pixels.size() != size.totalPixels()) {
        throw std::invalid_argument("Pixel array size (" + std::to_string(pixels.size()) +
                                    ") doesn't match expected dimensions (" +
                                    std::to_string(size.width) + "x" + std::to_string(size.height) +
                                    "x" + std::to_string(size.channels) + " = " +
                                    std::to_string(size.totalPixels()) + " pixels)");
    }
}

} // namespace nextcv::core
