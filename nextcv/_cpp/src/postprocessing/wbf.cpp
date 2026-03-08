#include "wbf.hpp"

#include <algorithm>
#include <array>
#include <cstddef>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

namespace nextcv::postprocessing {
namespace {

constexpr std::size_t box_data_size = 8U;
constexpr std::size_t label_index = 0U;
constexpr std::size_t score_index = 1U;
constexpr std::size_t weight_index = 2U;
constexpr std::size_t model_index = 3U;
constexpr std::size_t x1_index = 4U;
constexpr std::size_t y1_index = 5U;
constexpr std::size_t x2_index = 6U;
constexpr std::size_t y2_index = 7U;
constexpr std::size_t default_overall_boxes_reserve = 128U;

using BoxData =
    std::array<float, box_data_size>; // [label, score, weight, model_idx, x1, y1, x2, y2]

auto clamp01(float value) -> float {
    return std::clamp(value, 0.0F, 1.0F);
}

// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto iouXyxy(const BoxData& left, const BoxData& right) -> float {
    float ix1 = std::max(left[x1_index], right[x1_index]);
    float iy1 = std::max(left[y1_index], right[y1_index]);
    float ix2 = std::min(left[x2_index], right[x2_index]);
    float iy2 = std::min(left[y2_index], right[y2_index]);

    float inter_w = std::max(0.0F, ix2 - ix1);
    float inter_h = std::max(0.0F, iy2 - iy1);
    float inter = inter_w * inter_h;

    float area_left = (left[x2_index] - left[x1_index]) * (left[y2_index] - left[y1_index]);
    float area_right = (right[x2_index] - right[x1_index]) * (right[y2_index] - right[y1_index]);
    float denom = area_left + area_right - inter;
    if (denom <= 0.0F) {
        return 0.0F;
    }
    return inter / denom;
}

// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto prefilterBoxes(const std::vector<ModelBoxes>& boxes_list,
                    const std::vector<ModelScores>& scores_list,
                    const std::vector<ModelLabels>& labels_list, const std::vector<float>& weights,
                    float skip_box_thr) -> std::unordered_map<int, std::vector<BoxData>> {
    std::unordered_map<int, std::vector<BoxData>> filtered;

    for (std::size_t model_idx = 0; model_idx < boxes_list.size(); ++model_idx) {
        const auto& boxes = boxes_list[model_idx];
        const auto& scores = scores_list[model_idx];
        const auto& labels = labels_list[model_idx];

        if (boxes.size() != scores.size()) {
            throw std::invalid_argument(
                "Length mismatch: boxes and scores must have the same number of rows.");
        }
        if (boxes.size() != labels.size()) {
            throw std::invalid_argument(
                "Length mismatch: boxes and labels must have the same number of rows.");
        }

        for (std::size_t row = 0; row < boxes.size(); ++row) {
            float score = scores[row];
            if (score < skip_box_thr) {
                continue;
            }

            const auto& box = boxes[row];
            float x1 = box[0];
            float y1 = box[1];
            float x2 = box[2];
            float y2 = box[3];
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

            int label = labels[row];
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
        std::vector<std::size_t> sorted_indices(per_label_boxes.size());
        std::iota(sorted_indices.begin(), sorted_indices.end(), 0U);
        std::sort(sorted_indices.begin(), sorted_indices.end(),
                  [&](std::size_t left_idx, std::size_t right_idx) -> bool {
                      return per_label_boxes[left_idx][score_index] >
                             per_label_boxes[right_idx][score_index];
                  });
        std::vector<BoxData> sorted_boxes;
        sorted_boxes.reserve(per_label_boxes.size());
        for (std::size_t idx : sorted_indices) {
            sorted_boxes.push_back(per_label_boxes[idx]);
        }
        per_label_boxes = std::move(sorted_boxes);
    }

    return filtered;
}

// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto getWeightedBox(const std::vector<BoxData>& boxes, const std::string& conf_type) -> BoxData {
    if (boxes.empty()) {
        return BoxData{};
    }

    BoxData weighted{};
    float conf_sum = 0.0F;
    float weight_sum = 0.0F;
    float max_conf = boxes.front()[score_index];

    for (const auto& box : boxes) {
        weighted[x1_index] += box[score_index] * box[x1_index];
        weighted[y1_index] += box[score_index] * box[y1_index];
        weighted[x2_index] += box[score_index] * box[x2_index];
        weighted[y2_index] += box[score_index] * box[y2_index];
        conf_sum += box[score_index];
        weight_sum += box[weight_index];
        max_conf = std::max(max_conf, box[score_index]);
    }

    weighted[label_index] = boxes.front()[label_index];
    if (conf_type == "avg" || conf_type == "box_and_model_avg" ||
        conf_type == "absent_model_aware_avg") {
        weighted[score_index] = conf_sum / static_cast<float>(boxes.size());
    } else if (conf_type == "max") {
        weighted[score_index] = max_conf;
    } else {
        throw std::invalid_argument("Unknown conf_type.");
    }

    weighted[weight_index] = weight_sum;
    weighted[model_index] = -1.0F;

    if (conf_sum > 0.0F) {
        weighted[x1_index] /= conf_sum;
        weighted[y1_index] /= conf_sum;
        weighted[x2_index] /= conf_sum;
        weighted[y2_index] /= conf_sum;
    }

    return weighted;
}

// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto findMatchingBoxFast(const std::vector<BoxData>& weighted_boxes, const BoxData& candidate,
                         float iou_thr) -> std::pair<int, float> {
    int best_idx = -1;
    float best_iou = iou_thr;

    for (std::size_t idx = 0; idx < weighted_boxes.size(); ++idx) {
        if (weighted_boxes[idx][label_index] != candidate[label_index]) {
            continue;
        }
        float overlap = iouXyxy(weighted_boxes[idx], candidate);
        if (overlap > best_iou) {
            best_iou = overlap;
            best_idx = static_cast<int>(idx);
        }
    }

    return {best_idx, best_iou};
}

struct WeightStats {
    float sum = 0.0F;
    float max = 0.0F;
};

auto computeWeightStats(const std::vector<float>& effective_weights) -> WeightStats {
    WeightStats stats;
    for (float weight : effective_weights) {
        stats.sum += weight;
        stats.max = std::max(stats.max, weight);
    }
    return stats;
}

auto adjustClusterScore(BoxData& fused, const std::vector<BoxData>& cluster,
                        const std::vector<float>& effective_weights,
                        const WeightStats& weight_stats, const std::string& conf_type,
                        bool allows_overflow) -> void {
    if (conf_type == "box_and_model_avg") {
        fused[score_index] =
            fused[score_index] * static_cast<float>(cluster.size()) / fused[weight_index];
        std::set<int> unique_models;
        float unique_weight_sum = 0.0F;
        for (const auto& item : cluster) {
            int model_idx = static_cast<int>(item[model_index]);
            if (unique_models.insert(model_idx).second) {
                unique_weight_sum += item[weight_index];
            }
        }
        fused[score_index] = fused[score_index] * unique_weight_sum / weight_stats.sum;
        return;
    }

    if (conf_type == "absent_model_aware_avg") {
        std::set<int> present_models;
        for (const auto& item : cluster) {
            present_models.insert(static_cast<int>(item[model_index]));
        }
        float absent_weight_sum = 0.0F;
        for (std::size_t model_idx = 0; model_idx < effective_weights.size(); ++model_idx) {
            if (present_models.find(static_cast<int>(model_idx)) == present_models.end()) {
                absent_weight_sum += effective_weights[model_idx];
            }
        }
        fused[score_index] = fused[score_index] * static_cast<float>(cluster.size()) /
                             (fused[weight_index] + absent_weight_sum);
        return;
    }

    if (conf_type == "max") {
        fused[score_index] /= weight_stats.max;
        return;
    }

    if (!allows_overflow) {
        fused[score_index] *=
            static_cast<float>(std::min(effective_weights.size(), cluster.size())) /
            weight_stats.sum;
    } else {
        fused[score_index] *= static_cast<float>(cluster.size()) / weight_stats.sum;
    }
}

auto fuseOneLabel(const std::vector<BoxData>& boxes, float iou_thr,
                  const std::vector<float>& effective_weights, const WeightStats& weight_stats,
                  const std::string& conf_type, bool allows_overflow) -> std::vector<BoxData> {
    std::vector<std::vector<BoxData>> clustered_boxes;
    std::vector<BoxData> weighted_boxes;

    for (const auto& candidate : boxes) {
        auto [match_idx, _best_iou] = findMatchingBoxFast(weighted_boxes, candidate, iou_thr);
        if (match_idx != -1) {
            clustered_boxes[static_cast<std::size_t>(match_idx)].push_back(candidate);
            weighted_boxes[static_cast<std::size_t>(match_idx)] =
                getWeightedBox(clustered_boxes[static_cast<std::size_t>(match_idx)], conf_type);
            continue;
        }
        clustered_boxes.push_back({candidate});
        weighted_boxes.push_back(candidate);
    }

    for (std::size_t cluster_idx = 0; cluster_idx < clustered_boxes.size(); ++cluster_idx) {
        adjustClusterScore(weighted_boxes[cluster_idx], clustered_boxes[cluster_idx],
                           effective_weights, weight_stats, conf_type, allows_overflow);
    }

    return weighted_boxes;
}

auto sortByScoreDesc(const std::vector<BoxData>& boxes) -> std::vector<BoxData> {
    std::vector<std::size_t> sorted_indices(boxes.size());
    std::iota(sorted_indices.begin(), sorted_indices.end(), 0U);
    std::sort(sorted_indices.begin(), sorted_indices.end(),
              [&](std::size_t left_idx, std::size_t right_idx) -> bool {
                  return boxes[left_idx][score_index] > boxes[right_idx][score_index];
              });
    std::vector<BoxData> sorted_boxes;
    sorted_boxes.reserve(boxes.size());
    for (std::size_t idx : sorted_indices) {
        sorted_boxes.push_back(boxes[idx]);
    }
    return sorted_boxes;
}

} // namespace

// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)
auto weightedBoxesFusion(const std::vector<ModelBoxes>& boxes_list,
                         const std::vector<ModelScores>& scores_list,
                         const std::vector<ModelLabels>& labels_list,
                         const std::vector<float>& weights, float iou_thr, float skip_box_thr,
                         const std::string& conf_type, bool allows_overflow)
    -> std::tuple<ModelBoxes, ModelScores, ModelLabels> {
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
        prefilterBoxes(boxes_list, scores_list, labels_list, effective_weights, skip_box_thr);
    if (filtered.empty()) {
        return {ModelBoxes{}, ModelScores{}, ModelLabels{}};
    }

    WeightStats weight_stats = computeWeightStats(effective_weights);

    std::vector<BoxData> overall_boxes;
    overall_boxes.reserve(default_overall_boxes_reserve);

    for (const auto& [_, boxes] : filtered) {
        auto fused_label_boxes = fuseOneLabel(boxes, iou_thr, effective_weights, weight_stats,
                                              conf_type, allows_overflow);
        overall_boxes.insert(overall_boxes.end(), fused_label_boxes.begin(),
                             fused_label_boxes.end());
    }

    overall_boxes = sortByScoreDesc(overall_boxes);

    ModelBoxes fused_boxes;
    ModelScores fused_scores;
    ModelLabels fused_labels;
    fused_boxes.reserve(overall_boxes.size());
    fused_scores.reserve(overall_boxes.size());
    fused_labels.reserve(overall_boxes.size());

    for (const auto& item : overall_boxes) {
        fused_scores.push_back(item[score_index]);
        fused_labels.push_back(static_cast<int>(item[label_index]));
        fused_boxes.push_back({item[x1_index], item[y1_index], item[x2_index], item[y2_index]});
    }

    return {fused_boxes, fused_scores, fused_labels};
}

} // namespace nextcv::postprocessing
