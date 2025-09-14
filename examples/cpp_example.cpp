#include "core/hello.hpp"
#include "image/invert.hpp"
#include "postprocessing/nms.hpp"
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
    std::vector<nextcv::postprocessing::BoundingBox> boxes = {
        {10, 10, 50, 50, 0.9f},   // High confidence
        {15, 15, 45, 45, 0.8f},   // Overlapping, lower confidence
        {100, 100, 30, 30, 0.7f}, // Non-overlapping
        {20, 20, 40, 40, 0.6f}    // Overlapping, lowest confidence
    };

    std::cout << "Original boxes: " << boxes.size() << std::endl;
    for (const auto& box : boxes) {
        std::cout << "  (" << box.x << ", " << box.y << ", " << box.width << ", " << box.height
                  << ") conf=" << box.confidence << std::endl;
    }

    auto filtered_boxes = nextcv::postprocessing::nms(boxes, 0.5f);
    std::cout << "After NMS: " << filtered_boxes.size() << " boxes" << std::endl;
    for (const auto& box : filtered_boxes) {
        std::cout << "  (" << box.x << ", " << box.y << ", " << box.width << ", " << box.height
                  << ") conf=" << box.confidence << std::endl;
    }

    return 0;
}
