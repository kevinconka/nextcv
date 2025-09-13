#pragma once

#include "types.hpp"
#include <string>
#include <vector>

namespace nextcv {
namespace core {

// Utility functions
std::string get_version();
std::string get_build_info();

// Array validation utilities
bool is_valid_image_data(const PixelVector& data, const ImageSize& size);
bool is_contiguous_array(const PixelVector& data, const ImageSize& size);

// Memory utilities
PixelVector create_contiguous_copy(const PixelVector& data);
void validate_array_contiguity(const PixelVector& data, const ImageSize& size);

} // namespace core
} // namespace nextcv