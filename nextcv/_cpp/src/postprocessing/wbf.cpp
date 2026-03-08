#include "wbf.hpp"

#include <algorithm>
#include <array>
#include <cstddef>
#include <limits>
#include <set>
#include <stdexcept>
#include <unordered_map>
#include <utility>

namespace nextcv::postprocessing {
namespace {

using BoxData = std::array<float, 8>; // [label, score, weight, model_idx, x1, y1, x2, y2]

auto clamp01(float value) -> float {
    return std::clamp(value, 0.0F, 1.0F);
}

auto iou_xyxy(const BoxData& left, const BoxData& right) -> float {
    float ix1 = std::max(left[4], right[4]);
    float iy1 = std::max(left[5], right[5]);
    float ix2 = std::min(left[6], right[6]);
    float iy2 = std::min(left[7], right[7]);

    float inter_w = std::max(0.0F, ix2 - ix1);
    float inter_h = std::max(0.0F, iy2 - iy1);
    float inter = inter_w * inter_h;

    float area_left = (left[6] - left[4]) * (left[7] - left[5]);
    float area_right = (right[6] - right[4]) * (right[7] - right[5]);
    float denom = area_left + area_right - inter;
    if (denom <= 0.0F) {
        return 0.0F;
    }
    return inter / denom;
}

auto prefilter_boxes(const std::vector<Eigen::MatrixXf>& boxes_list,
                     const std::vector<Eigen::VectorXf>& scores_list,
                     const std::vector<Eigen::VectorXi>& labels_list,
                     const std::vector<float>& weights, float skip_box_thr)
    -> std::unordered_map<int, std::vector<BoxData>> {
    std::unordered_map<int, std::vector<BoxData>> filtered;

    for (std::size_t model_idx = 0; model_idx < boxes_list.size(); ++model_idx) {
        const auto& boxes = boxes_list[model_idx];
        const auto& scores = scores_list[model_idx];
        const auto& labels = labels_list[model_idx];

        if (boxes.cols() != 4) {
            throw std::invalid_argument("Each boxes_list element must be shaped (N, 4).");
        }
        if (boxes.rows() != scores.size()) {
            throw std::invalid_argument(
                "Length mismatch: boxes and scores must have the same number of rows.");
        }
        if (boxes.rows() != labels.size()) {
            throw std::invalid_argument(
                "Length mismatch: boxes and labels must have the same number of rows.");
        }

        for (int row = 0; row < boxes.rows(); ++row) {
            float score = scores(row);
            if (score < skip_box_thr) {
                continue;
            }

            float x1 = boxes(row, 0);
            float y1 = boxes(row, 1);
            float x2 = boxes(row, 2);
            float y2 = boxes(row, 3);
            if (x2 < x1) {
                std::swap(x1, x2);
            }
            if (y2 < y1) {
                std::swap(y1, y2);
            }

            x1 = clamp01(x1);
            y1 = clamp01(y1);
            x2 = clamp01(x2);
            y2 = clamp01(y2);

            if ((x2 - x1) * (y2 - y1) <= 0.0F) {
                continue;
            }

            int label = labels(row);
            BoxData candidate = {static_cast<float>(label),
                                 score * weights[model_idx],
                                 weights[model_idx],
                                 static_cast<float>(model_idx),
                                 x1,
                                 y1,
                                 x2,
                                 y2};
            filtered[label].push_back(candidate);
        }
    }

    for (auto& [_, per_label_boxes] : filtered) {
        std::sort(
            per_label_boxes.begin(), per_label_boxes.end(),
            [](const BoxData& left, const BoxData& right) -> bool { return left[1] > right[1]; });
    }

    return filtered;
}

auto get_weighted_box(const std::vector<BoxData>& boxes, const std::string& conf_type) -> BoxData {
    if (boxes.empty()) {
        return BoxData{};
    }

    BoxData weighted{};
    float conf_sum = 0.0F;
    float weight_sum = 0.0F;
    float max_conf = std::numeric_limits<float>::lowest();

    for (const auto& box : boxes) {
        weighted[4] += box[1] * box[4];
        weighted[5] += box[1] * box[5];
        weighted[6] += box[1] * box[6];
        weighted[7] += box[1] * box[7];
        conf_sum += box[1];
        weight_sum += box[2];
        max_conf = std::max(max_conf, box[1]);
    }

    weighted[0] = boxes.front()[0];
    if (conf_type == "avg" || conf_type == "box_and_model_avg" ||
        conf_type == "absent_model_aware_avg") {
        weighted[1] = conf_sum / static_cast<float>(boxes.size());
    } else if (conf_type == "max") {
        weighted[1] = max_conf;
    } else {
        throw std::invalid_argument("Unknown conf_type.");
    }

    weighted[2] = weight_sum;
    weighted[3] = -1.0F;

    if (conf_sum > 0.0F) {
        weighted[4] /= conf_sum;
        weighted[5] /= conf_sum;
        weighted[6] /= conf_sum;
        weighted[7] /= conf_sum;
    }

    return weighted;
}

auto find_matching_box_fast(const std::vector<BoxData>& weighted_boxes, const BoxData& candidate,
                            float iou_thr) -> std::pair<int, float> {
    int best_idx = -1;
    float best_iou = iou_thr;

    for (std::size_t idx = 0; idx < weighted_boxes.size(); ++idx) {
        if (weighted_boxes[idx][0] != candidate[0]) {
            continue;
        }
        float overlap = iou_xyxy(weighted_boxes[idx], candidate);
        if (overlap > best_iou) {
            best_iou = overlap;
            best_idx = static_cast<int>(idx);
        }
    }

    return {best_idx, best_iou};
}

} // namespace

auto weighted_boxes_fusion(const std::vector<Eigen::MatrixXf>& boxes_list,
                           const std::vector<Eigen::VectorXf>& scores_list,
                           const std::vector<Eigen::VectorXi>& labels_list,
                           const std::vector<float>& weights, float iou_thr, float skip_box_thr,
                           const std::string& conf_type, bool allows_overflow)
    -> std::tuple<Eigen::MatrixXf, Eigen::VectorXf, Eigen::VectorXi> {
    if (boxes_list.size() != scores_list.size() || boxes_list.size() != labels_list.size()) {
        throw std::invalid_argument(
            "boxes_list, scores_list, and labels_list must have equal length.");
    }

    std::vector<float> effective_weights = weights;
    if (effective_weights.empty() || effective_weights.size() != boxes_list.size()) {
        effective_weights.assign(boxes_list.size(), 1.0F);
    }

    if (conf_type != "avg" && conf_type != "max" && conf_type != "box_and_model_avg" &&
        conf_type != "absent_model_aware_avg") {
        throw std::invalid_argument(
            "conf_type must be one of: avg, max, box_and_model_avg, absent_model_aware_avg.");
    }

    auto filtered =
        prefilter_boxes(boxes_list, scores_list, labels_list, effective_weights, skip_box_thr);
    if (filtered.empty()) {
        return {Eigen::MatrixXf(0, 4), Eigen::VectorXf(0), Eigen::VectorXi(0)};
    }

    float weights_sum = 0.0F;
    float max_weight = 0.0F;
    for (float weight : effective_weights) {
        weights_sum += weight;
        max_weight = std::max(max_weight, weight);
    }

    std::vector<BoxData> overall_boxes;
    overall_boxes.reserve(128);

    for (auto& [_, boxes] : filtered) {
        std::vector<std::vector<BoxData>> clustered_boxes;
        std::vector<BoxData> weighted_boxes;

        for (const auto& candidate : boxes) {
            auto [match_idx, _best_iou] =
                find_matching_box_fast(weighted_boxes, candidate, iou_thr);
            if (match_idx != -1) {
                clustered_boxes[static_cast<std::size_t>(match_idx)].push_back(candidate);
                weighted_boxes[static_cast<std::size_t>(match_idx)] = get_weighted_box(
                    clustered_boxes[static_cast<std::size_t>(match_idx)], conf_type);
            } else {
                clustered_boxes.push_back({candidate});
                weighted_boxes.push_back(candidate);
            }
        }

        for (std::size_t cluster_idx = 0; cluster_idx < clustered_boxes.size(); ++cluster_idx) {
            auto& cluster = clustered_boxes[cluster_idx];
            auto& fused = weighted_boxes[cluster_idx];

            if (conf_type == "box_and_model_avg") {
                fused[1] = fused[1] * static_cast<float>(cluster.size()) / fused[2];
                std::set<int> unique_models;
                float unique_weight_sum = 0.0F;
                for (const auto& item : cluster) {
                    int model_idx = static_cast<int>(item[3]);
                    if (unique_models.insert(model_idx).second) {
                        unique_weight_sum += item[2];
                    }
                }
                fused[1] = fused[1] * unique_weight_sum / weights_sum;
            } else if (conf_type == "absent_model_aware_avg") {
                std::set<int> present_models;
                for (const auto& item : cluster) {
                    present_models.insert(static_cast<int>(item[3]));
                }
                float absent_weight_sum = 0.0F;
                for (std::size_t model_idx = 0; model_idx < effective_weights.size(); ++model_idx) {
                    if (present_models.find(static_cast<int>(model_idx)) == present_models.end()) {
                        absent_weight_sum += effective_weights[model_idx];
                    }
                }
                fused[1] =
                    fused[1] * static_cast<float>(cluster.size()) / (fused[2] + absent_weight_sum);
            } else if (conf_type == "max") {
                fused[1] /= max_weight;
            } else if (!allows_overflow) {
                fused[1] *= static_cast<float>(std::min(effective_weights.size(), cluster.size())) /
                            weights_sum;
            } else {
                fused[1] *= static_cast<float>(cluster.size()) / weights_sum;
            }
        }

        overall_boxes.insert(overall_boxes.end(), weighted_boxes.begin(), weighted_boxes.end());
    }

    std::sort(overall_boxes.begin(), overall_boxes.end(),
              [](const BoxData& left, const BoxData& right) -> bool { return left[1] > right[1]; });

    Eigen::MatrixXf fused_boxes(static_cast<int>(overall_boxes.size()), 4);
    Eigen::VectorXf fused_scores(static_cast<int>(overall_boxes.size()));
    Eigen::VectorXi fused_labels(static_cast<int>(overall_boxes.size()));

    for (std::size_t row = 0; row < overall_boxes.size(); ++row) {
        const auto& item = overall_boxes[row];
        fused_scores(static_cast<int>(row)) = item[1];
        fused_labels(static_cast<int>(row)) = static_cast<int>(item[0]);
        fused_boxes(static_cast<int>(row), 0) = item[4];
        fused_boxes(static_cast<int>(row), 1) = item[5];
        fused_boxes(static_cast<int>(row), 2) = item[6];
        fused_boxes(static_cast<int>(row), 3) = item[7];
    }

    return {fused_boxes, fused_scores, fused_labels};
}

} // namespace nextcv::postprocessing
