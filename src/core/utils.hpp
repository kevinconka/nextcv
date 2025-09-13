#pragma once

#include "types.hpp"
#include <string>

namespace nextcv {

// Utility functions
std::string get_version();
std::string get_build_info();

// Array validation utilities
bool is_valid_image_data(const PixelVector& data, const ImageSize& size);
void validate_array_contiguity(const PixelVector& data, const ImageSize& size);

} // namespace nextcv