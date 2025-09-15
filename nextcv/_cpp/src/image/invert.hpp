#pragma once

#include "../core/types.hpp"

namespace nextcv::image {

/**
 * @brief Invert pixel values in an image
 * @param pixels Input pixel data
 * @return Inverted pixel data
 */
auto invert(const core::PixelVector& pixels) -> core::PixelVector;

} // namespace nextcv::image
