#pragma once

#include "../../core/types.hpp"
#include <vector>

namespace nextcv {
namespace image {
namespace operations {

/**
 * @brief Invert pixel values in an image
 * @param pixels Input pixel data
 * @return Inverted pixel data
 */
PixelVector invert(const PixelVector& pixels);

/**
 * @brief Invert pixel values with validation
 * @param pixels Input pixel data
 * @param size Expected image dimensions
 * @return Inverted pixel data
 * @throws std::invalid_argument if data size doesn't match expected dimensions
 */
PixelVector invert(const PixelVector& pixels, const core::ImageSize& size);

} // namespace operations
} // namespace image
} // namespace nextcv