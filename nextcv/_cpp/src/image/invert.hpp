#pragma once

#include "../core/types.hpp"

namespace nextcv::image {

/**
 * @brief Invert pixel values in an image
 * @param pixels Input pixel data
 * @return Inverted pixel data
 */
auto invert(const core::PixelVector& pixels) -> core::PixelVector;

/**
 * @brief Invert pixel values with validation
 * @param pixels Input pixel data
 * @param size Expected image dimensions
 * @return Inverted pixel data
 * @throws std::invalid_argument if data size doesn't match expected dimensions
 */
auto invert(const core::PixelVector& pixels, const core::ImageSize& size) -> core::PixelVector;

} // namespace nextcv::image
