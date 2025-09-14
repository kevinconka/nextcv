#pragma once

#include "../core/types.hpp"

namespace nextcv {
namespace image {

/**
 * @brief Invert pixel values in an image
 * @param pixels Input pixel data
 * @return Inverted pixel data
 */
core::PixelVector invert(const core::PixelVector& pixels);

/**
 * @brief Invert pixel values with validation
 * @param pixels Input pixel data
 * @param size Expected image dimensions
 * @return Inverted pixel data
 * @throws std::invalid_argument if data size doesn't match expected dimensions
 */
core::PixelVector invert(const core::PixelVector& pixels, const core::ImageSize& size);

} // namespace image
} // namespace nextcv
