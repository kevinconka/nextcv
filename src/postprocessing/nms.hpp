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
 * @brief Apply Non-Maximum Suppression to bounding boxes (numpy array version)
 * @param bboxes Bounding boxes as (x1, y1, x2, y2) format
 * @param scores Confidence scores for each bounding box
 * @param threshold IoU threshold for suppression
 * @return Indices of boxes to keep after NMS
 */
std::vector<int> nms(const std::vector<std::array<float, 4>>& bboxes,
                     const std::vector<float>& scores, float threshold = 0.5f);

} // namespace postprocessing
} // namespace nextcv
