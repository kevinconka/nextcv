#include "nms.hpp"
#include <algorithm>
#include <vector>

namespace nextcv {
namespace postprocessing {

std::vector<BoundingBox> nms(const std::vector<BoundingBox>& boxes, float threshold) {
    if (boxes.empty()) {
        return {};
    }

    // Sort boxes by confidence (descending)
    std::vector<BoundingBox> sorted_boxes = boxes;
    std::sort(
        sorted_boxes.begin(), sorted_boxes.end(),
        [](const BoundingBox& a, const BoundingBox& b) { return a.confidence > b.confidence; });

    std::vector<BoundingBox> result;
    std::vector<bool> suppressed(sorted_boxes.size(), false);

    for (size_t i = 0; i < sorted_boxes.size(); ++i) {
        if (suppressed[i])
            continue;

        result.push_back(sorted_boxes[i]);

        // Suppress boxes with high IoU
        for (size_t j = i + 1; j < sorted_boxes.size(); ++j) {
            if (suppressed[j])
                continue;

            // Calculate IoU (simplified - just overlap check for demo)
            const auto& box1 = sorted_boxes[i];
            const auto& box2 = sorted_boxes[j];

            float overlap = std::max(0.0f, std::min(box1.x + box1.width, box2.x + box2.width) -
                                               std::max(box1.x, box2.x)) *
                            std::max(0.0f, std::min(box1.y + box1.height, box2.y + box2.height) -
                                               std::max(box1.y, box2.y));

            float area1 = box1.width * box1.height;
            float area2 = box2.width * box2.height;
            float iou = overlap / (area1 + area2 - overlap);

            if (iou > threshold) {
                suppressed[j] = true;
            }
        }
    }

    return result;
}

} // namespace postprocessing
} // namespace nextcv
