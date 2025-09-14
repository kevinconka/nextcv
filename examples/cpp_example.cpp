#include "nextcv/core/hello.hpp"
#include "nextcv/image/invert.hpp"
#include "nextcv/postprocessing/nms.hpp"
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    // Demonstrate hello functionality
    std::cout << "=== NextCV C++ Example ===" << std::endl;
    std::cout << nextcv::core::hello() << std::endl;

    // Demonstrate invert functionality
    std::cout << "\n=== Pixel Inversion Demo ===" << std::endl;
    std::vector<std::uint8_t> pixels{0, 64, 128, 192, 255};

    std::cout << "Original pixels: ";
    for (auto v : pixels) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;

    auto inverted = nextcv::image::invert(pixels);

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
    auto single_inverted = nextcv::image::invert(single_pixel);
    std::cout << "100 -> " << static_cast<int>(single_inverted[0]) << " (expected: " << (255 - 100)
              << ")" << std::endl;

    // Demonstrate NMS functionality
    std::cout << "\n=== NMS Demo ===" << std::endl;
    std::vector<std::array<float, 4>> bboxes = {
        {10, 10, 60, 60},     // x1, y1, x2, y2 - High confidence
        {15, 15, 60, 60},     // Overlapping, lower confidence
        {100, 100, 130, 130}, // Non-overlapping
        {20, 20, 60, 60}      // Overlapping, lowest confidence
    };
    std::vector<float> scores = {0.9f, 0.8f, 0.7f, 0.6f};

    std::cout << "Original boxes: " << bboxes.size() << std::endl;
    for (size_t i = 0; i < bboxes.size(); ++i) {
        const auto& box = bboxes[i];
        std::cout << "  [" << i << "] (" << box[0] << ", " << box[1] << ", " << box[2] << ", "
                  << box[3] << ") conf=" << scores[i] << std::endl;
    }

    auto kept_indices = nextcv::postprocessing::nms(bboxes, scores, 0.5f);
    std::cout << "After NMS: " << kept_indices.size() << " boxes kept" << std::endl;
    for (const auto& idx : kept_indices) {
        const auto& box = bboxes[static_cast<size_t>(idx)];
        std::cout << "  [" << idx << "] (" << box[0] << ", " << box[1] << ", " << box[2] << ", "
                  << box[3] << ") conf=" << scores[static_cast<size_t>(idx)] << std::endl;
    }

    return 0;
}
