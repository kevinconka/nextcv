#pragma once

#include <array>
#include <vector>

namespace nextcv::postprocessing {

// Default IoU threshold for NMS
constexpr float default_nms_threshold = 0.5F;

/**
 * @brief Apply Non-Maximum Suppression to bounding boxes (numpy array version)
 * @param bboxes Bounding boxes as (x1, y1, x2, y2) format
 * @param scores Confidence scores for each bounding box
 * @param threshold IoU threshold for suppression
 * @return Indices of boxes to keep after NMS
 */
auto nms(const std::vector<std::array<float, 4>>& bboxes, const std::vector<float>& scores,
         float threshold = default_nms_threshold) -> std::vector<int>;

} // namespace nextcv::postprocessing
