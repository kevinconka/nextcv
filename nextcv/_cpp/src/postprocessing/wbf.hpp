#pragma once

#include <Eigen/Core>
#include <string>
#include <tuple>
#include <vector>

namespace nextcv::postprocessing {

constexpr float default_wbf_iou_threshold = 0.55F;
constexpr float default_wbf_skip_box_threshold = 0.0F;
constexpr const char* default_wbf_conf_type = "avg";

/**
 * @brief Apply Weighted Box Fusion (WBF) to model predictions.
 *
 * Mirrors the behavior of the reference implementation from
 * `ensemble_boxes_wbf.py` for normalized boxes in [0, 1].
 *
 * @param boxes_list Per-model bounding boxes in (x1, y1, x2, y2) format.
 * @param scores_list Per-model confidence scores.
 * @param labels_list Per-model class labels.
 * @param weights Optional per-model weights (defaults to 1.0 for each model).
 * @param iou_thr IoU threshold for matching boxes into a cluster.
 * @param skip_box_thr Skip boxes with score lower than this threshold.
 * @param conf_type Confidence mode:
 *   "avg", "max", "box_and_model_avg", "absent_model_aware_avg".
 * @param allows_overflow If true, confidence can exceed 1.0 for "avg" mode.
 *
 * @return Tuple of (fused_boxes, fused_scores, fused_labels).
 */
auto weightedBoxesFusion(
    const std::vector<Eigen::MatrixXf>& boxes_list, const std::vector<Eigen::VectorXf>& scores_list,
    const std::vector<Eigen::VectorXi>& labels_list, const std::vector<float>& weights = {},
    float iou_thr = default_wbf_iou_threshold, float skip_box_thr = default_wbf_skip_box_threshold,
    const std::string& conf_type = default_wbf_conf_type, bool allows_overflow = false)
    -> std::tuple<Eigen::MatrixXf, Eigen::VectorXf,
                  Eigen::VectorXi>; // NOLINT(bugprone-easily-swappable-parameters)

} // namespace nextcv::postprocessing
