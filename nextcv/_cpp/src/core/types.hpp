#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace nextcv::core {

// Common type definitions
using Pixel = std::uint8_t;
using PixelVector = std::vector<Pixel>;

// Image dimensions
struct ImageSize {
    std::size_t width;
    std::size_t height;
    std::size_t channels;

    ImageSize(std::size_t w, std::size_t h, std::size_t c = 1) : width(w), height(h), channels(c) {}

    [[nodiscard]] auto totalPixels() const -> std::size_t {
        return width * height * channels;
    }
};

// Color space definitions
enum class ColorSpace { GRAYSCALE = 1, RGB = 3, RGBA = 4, BGR = 3, BGRA = 4 };

} // namespace nextcv::core
