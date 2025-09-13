#pragma once

#include "../core/types.hpp"

namespace nextcv {

/**
 * @brief Apply binary threshold to image
 * @param pixels Input pixel data
 * @param threshold Threshold value (0-255)
 * @param max_value Value to assign to pixels above threshold
 * @return Thresholded pixel data
 */
PixelVector threshold(const PixelVector& pixels, Pixel threshold, Pixel max_value = 255);

/**
 * @brief Apply binary threshold with validation
 * @param pixels Input pixel data
 * @param size Expected image dimensions
 * @param threshold Threshold value (0-255)
 * @param max_value Value to assign to pixels above threshold
 * @return Thresholded pixel data
 */
PixelVector threshold(const PixelVector& pixels, const ImageSize& size, 
                     Pixel threshold, Pixel max_value = 255);

} // namespace nextcv