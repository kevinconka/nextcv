#include "nms.hpp"
#include <algorithm>
#include <array>
#include <numeric>
#include <vector>

namespace nextcv {
namespace postprocessing {

std::vector<int> nms(const std::vector<std::array<float, 4>>& bboxes,
                     const std::vector<float>& scores, float threshold) {
    if (bboxes.empty() || scores.empty() || bboxes.size() != scores.size()) {
        return {};
    }

    // Create indices and sort by scores (descending)
    std::vector<int> indices(bboxes.size());
    std::iota(indices.begin(), indices.end(), 0);

    std::sort(indices.begin(), indices.end(),
              [&scores](int a, int b) { return scores[a] > scores[b]; });

    std::vector<int> result;
    std::vector<bool> suppressed(bboxes.size(), false);

    for (size_t i = 0; i < indices.size(); ++i) {
        if (suppressed[indices[i]])
            continue;

        result.push_back(indices[i]);

        // Suppress boxes with high IoU
        for (size_t j = i + 1; j < indices.size(); ++j) {
            if (suppressed[indices[j]])
                continue;

            // Calculate IoU
            const auto& box1 = bboxes[indices[i]];
            const auto& box2 = bboxes[indices[j]];

            // Intersection
            float x1 = std::max(box1[0], box2[0]);
            float y1 = std::max(box1[1], box2[1]);
            float x2 = std::min(box1[2], box2[2]);
            float y2 = std::min(box1[3], box2[3]);

            float intersection = std::max(0.0f, x2 - x1) * std::max(0.0f, y2 - y1);

            // Areas
            float area1 = (box1[2] - box1[0]) * (box1[3] - box1[1]);
            float area2 = (box2[2] - box2[0]) * (box2[3] - box2[1]);
            float union_area = area1 + area2 - intersection;

            float iou = intersection / union_area;

            if (iou > threshold) {
                suppressed[indices[j]] = true;
            }
        }
    }

    return result;
}

} // namespace postprocessing
} // namespace nextcv
