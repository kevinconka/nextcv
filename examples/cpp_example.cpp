#include "core/hello.hpp"
#include "imgproc/invert.hpp"
#include "imgproc/threshold.hpp"
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    // Demonstrate hello functionality
    std::cout << "=== NextCV C++ Example ===" << std::endl;
    std::cout << nextcv::hello() << std::endl;

    // Demonstrate invert functionality
    std::cout << "\n=== Pixel Inversion Demo ===" << std::endl;
    std::vector<std::uint8_t> pixels{0, 64, 128, 192, 255};

    std::cout << "Original pixels: ";
    for (auto v : pixels) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;

    auto inverted = nextcv::invert(pixels);

    std::cout << "Inverted pixels: ";
    for (auto v : inverted) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;

    // Verify the inversion worked correctly
    std::vector<std::uint8_t> expected{255, 191, 127, 63, 0};
    bool correct = (inverted == expected);
    std::cout << "Verification: " << (correct ? "PASSED" : "FAILED") << std::endl;

    // Demonstrate with a single pixel
    std::cout << "\n=== Single Pixel Test ===" << std::endl;
    std::vector<std::uint8_t> single_pixel{100};
    auto single_inverted = nextcv::invert(single_pixel);
    std::cout << "100 -> " << static_cast<int>(single_inverted[0]) << " (expected: " << (255 - 100)
              << ")" << std::endl;

    // Demonstrate threshold functionality
    std::cout << "\n=== Threshold Demo ===" << std::endl;
    std::vector<std::uint8_t> test_pixels{50, 100, 150, 200, 250};
    std::cout << "Original pixels: ";
    for (auto v : test_pixels) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;

    auto thresholded = nextcv::threshold(test_pixels, 128);
    std::cout << "Thresholded (128): ";
    for (auto v : thresholded) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;

    return 0;
}