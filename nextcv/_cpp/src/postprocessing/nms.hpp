#pragma once

#include <Eigen/Core>
#include <vector>

namespace nextcv::postprocessing {

// Default IoU threshold for NMS
constexpr float default_nms_threshold = 0.5F;

/**
 * @brief Apply Non-Maximum Suppression to bounding boxes (Eigen version)
 * @param bboxes Bounding boxes as (x1, y1, x2, y2) format, Nx4 matrix
 * @param scores Confidence scores for each bounding box, Nx1 vector
 * @param threshold IoU threshold for suppression
 * @return Indices of boxes to keep after NMS
 */
// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto nms(const Eigen::MatrixXf& bboxes, const Eigen::VectorXf& scores,
         float threshold = default_nms_threshold) -> std::vector<int>;

} // namespace nextcv::postprocessing
