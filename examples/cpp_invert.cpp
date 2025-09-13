#include "invert.hpp"
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    std::vector<std::uint8_t> pixels{0, 64, 128, 192, 255};
    auto inv = nextcv::invert(pixels);
    for (auto v : inv) {
        std::cout << static_cast<int>(v) << " ";
    }
    std::cout << std::endl;
    return 0;
}
