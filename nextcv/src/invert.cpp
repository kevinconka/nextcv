#include "invert.hpp"

namespace nextcv {

std::vector<std::uint8_t> invert(const std::vector<std::uint8_t>& pixels) {
    std::vector<std::uint8_t> out;
    out.reserve(pixels.size());
    for (std::uint8_t p : pixels) {
        out.push_back(static_cast<std::uint8_t>(255 - p));
    }
    return out;
}

} // namespace nextcv

