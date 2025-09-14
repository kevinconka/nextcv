#pragma once

#include "../core/types.hpp"
#include <vector>

namespace nextcv {
namespace postprocessing {

// Bounding box structure
struct BoundingBox {
    float x, y, width, height;
    float confidence;

    BoundingBox(float x, float y, float w, float h, float conf)
        : x(x), y(y), width(w), height(h), confidence(conf) {}
};

/**
 * @brief Apply Non-Maximum Suppression to bounding boxes
 * @param boxes Input bounding boxes
 * @param threshold IoU threshold for suppression
 * @return Filtered bounding boxes after NMS
 */
std::vector<BoundingBox> nms(const std::vector<BoundingBox>& boxes, float threshold = 0.5f);

} // namespace postprocessing
} // namespace nextcv
