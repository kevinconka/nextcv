#include "wbf.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <unordered_map>
#include <vector>

#if defined(__cplusplus) && (__cplusplus >= 202002L)
#if defined(__has_include)
#if __has_include(<ranges>)
#include <ranges>
#define NEXTCV_HAS_RANGES 1
#else
#define NEXTCV_HAS_RANGES 0
#endif
#else
#define NEXTCV_HAS_RANGES 0
#endif
#else
#define NEXTCV_HAS_RANGES 0
#endif

namespace nextcv::postprocessing {
namespace {

constexpr std::size_t default_overall_boxes_reserve = 128U;

struct Box {
    float x1 = 0.0F;
    float y1 = 0.0F;
    float x2 = 0.0F;
    float y2 = 0.0F;
};

struct CandidateBox {
    int label = 0;
    float score = 0.0F;
    float weight = 0.0F;
    int model_idx = -1;
    Box box{};
};

struct Cluster {
    std::vector<CandidateBox> members;
    CandidateBox fused;
};

enum class ConfidenceType : std::uint8_t {
    AVG,
    MAX,
    BOX_AND_MODEL_AVG,
    ABSENT_MODEL_AWARE_AVG,
};

auto clamp01(float value) -> float {
    return std::clamp(value, 0.0F, 1.0F);
}

auto parseConfidenceType(std::string_view conf_type) -> ConfidenceType {
    static const std::unordered_map<std::string_view, ConfidenceType> conf_type_map = {
        {"avg", ConfidenceType::AVG},
        {"max", ConfidenceType::MAX},
        {"box_and_model_avg", ConfidenceType::BOX_AND_MODEL_AVG},
        {"absent_model_aware_avg", ConfidenceType::ABSENT_MODEL_AWARE_AVG},
    };

    const auto it = conf_type_map.find(conf_type);
    if (it != conf_type_map.end()) {
        return it->second;
    }
    throw std::invalid_argument(
        "conf_type must be one of: avg, max, box_and_model_avg, absent_model_aware_avg.");
}

auto normalizeBox(float x1, float y1, float x2, float y2) -> Box {
    if (x2 < x1) {
        std::swap(x1, x2);
    }
    if (y2 < y1) {
        std::swap(y1, y2);
    }
    return Box{
        .x1 = clamp01(x1),
        .y1 = clamp01(y1),
        .x2 = clamp01(x2),
        .y2 = clamp01(y2),
    };
}

auto isValidBox(const Box& box) -> bool {
    return (box.x2 - box.x1) * (box.y2 - box.y1) > 0.0F;
}

auto makeCandidateBox(int label, float score, float model_weight, int model_idx, const Box& box)
    -> CandidateBox {
    return CandidateBox{
        .label = label,
        .score = score * model_weight,
        .weight = model_weight,
        .model_idx = model_idx,
        .box = box,
    };
}

auto iouXyxy(const Box& left, const Box& right)
    -> float { // NOLINT(bugprone-easily-swappable-parameters)
    float ix1 = std::max(left.x1, right.x1);
    float iy1 = std::max(left.y1, right.y1);
    float ix2 = std::min(left.x2, right.x2);
    float iy2 = std::min(left.y2, right.y2);

    float inter_w = std::max(0.0F, ix2 - ix1);
    float inter_h = std::max(0.0F, iy2 - iy1);
    float inter = inter_w * inter_h;

    float area_left = (left.x2 - left.x1) * (left.y2 - left.y1);
    float area_right = (right.x2 - right.x1) * (right.y2 - right.y1);
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
                    float skip_box_thr) // NOLINT(bugprone-easily-swappable-parameters)
    -> std::unordered_map<int, std::vector<CandidateBox>> {
    std::unordered_map<int, std::vector<CandidateBox>> boxes_by_label;

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

        const auto process_row = [&](std::size_t row) -> void {
            float score = scores[row];

            const auto& box = boxes[row];
            const Box normalized_box = normalizeBox(box[0], box[1], box[2], box[3]);
            if (!isValidBox(normalized_box)) {
                return;
            }

            int label = labels[row];
            const CandidateBox candidate = makeCandidateBox(
                label, score, weights[model_idx], static_cast<int>(model_idx), normalized_box);
            boxes_by_label[label].push_back(candidate);
        };

#if NEXTCV_HAS_RANGES
        auto row_indices = std::views::iota(std::size_t{0}, boxes.size()) |
                           std::views::filter([&scores, skip_box_thr](std::size_t row) {
                               return scores[row] >= skip_box_thr;
                           });
        for (std::size_t row : row_indices) {
            process_row(row);
        }
#else
        for (std::size_t row = 0; row < boxes.size(); ++row) {
            if (scores[row] < skip_box_thr) {
                continue;
            }
            process_row(row);
        }
#endif
    }

    for (auto& [_, per_label_boxes] : boxes_by_label) {
#if NEXTCV_HAS_RANGES
        std::ranges::sort(per_label_boxes, [](const CandidateBox& left, const CandidateBox& right) {
            return left.score > right.score;
        });
#else
        std::sort(per_label_boxes.begin(), per_label_boxes.end(),
                  [](const CandidateBox& left, const CandidateBox& right) -> bool {
                      return left.score > right.score;
                  });
#endif
    }

    return boxes_by_label;
}

auto computeWeightedBox(const std::vector<CandidateBox>& boxes, ConfidenceType conf_type)
    -> CandidateBox {
    if (boxes.empty()) {
        return CandidateBox{};
    }

    CandidateBox weighted{};
    float conf_sum = 0.0F;
    float weight_sum = 0.0F;
    float max_conf = boxes.front().score;

    for (const auto& candidate : boxes) {
        weighted.box.x1 += candidate.score * candidate.box.x1;
        weighted.box.y1 += candidate.score * candidate.box.y1;
        weighted.box.x2 += candidate.score * candidate.box.x2;
        weighted.box.y2 += candidate.score * candidate.box.y2;
        conf_sum += candidate.score;
        weight_sum += candidate.weight;
        max_conf = std::max(max_conf, candidate.score);
    }

    weighted.label = boxes.front().label;
    switch (conf_type) {
    case ConfidenceType::AVG:
    case ConfidenceType::BOX_AND_MODEL_AVG:
    case ConfidenceType::ABSENT_MODEL_AWARE_AVG:
        weighted.score = conf_sum / static_cast<float>(boxes.size());
        break;
    case ConfidenceType::MAX:
        weighted.score = max_conf;
        break;
    }

    weighted.weight = weight_sum;
    weighted.model_idx = -1;

    if (conf_sum > 0.0F) {
        weighted.box.x1 /= conf_sum;
        weighted.box.y1 /= conf_sum;
        weighted.box.x2 /= conf_sum;
        weighted.box.y2 /= conf_sum;
    }

    return weighted;
}

auto findBestMatchingCluster(const std::vector<Cluster>& clusters, const CandidateBox& candidate,
                             float iou_thr) -> int {
    int best_idx = -1;
    float best_iou = iou_thr;

    for (std::size_t idx = 0; idx < clusters.size(); ++idx) {
        float overlap = iouXyxy(clusters[idx].fused.box, candidate.box);
        if (overlap > best_iou) {
            best_iou = overlap;
            best_idx = static_cast<int>(idx);
        }
    }

    return best_idx;
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

auto adjustClusterScore(CandidateBox& fused, const std::vector<CandidateBox>& cluster,
                        const std::vector<float>& effective_weights,
                        const WeightStats& weight_stats, ConfidenceType conf_type,
                        bool allows_overflow) // NOLINT(bugprone-easily-swappable-parameters)
    -> void {
    switch (conf_type) {
    case ConfidenceType::BOX_AND_MODEL_AVG: {
        fused.score = fused.score * static_cast<float>(cluster.size()) / fused.weight;
        std::vector<bool> model_present(effective_weights.size(), false);
        float unique_weight_sum = 0.0F;
        for (const auto& member : cluster) {
            const auto model_idx = static_cast<std::size_t>(member.model_idx);
            if (!model_present[model_idx]) {
                model_present[model_idx] = true;
                unique_weight_sum += effective_weights[model_idx];
            }
        }
        fused.score = fused.score * unique_weight_sum / weight_stats.sum;
        return;
    }

    case ConfidenceType::ABSENT_MODEL_AWARE_AVG: {
        std::vector<bool> model_present(effective_weights.size(), false);
        for (const auto& member : cluster) {
            model_present[static_cast<std::size_t>(member.model_idx)] = true;
        }
        float absent_weight_sum = 0.0F;
        for (std::size_t model_idx = 0; model_idx < effective_weights.size(); ++model_idx) {
            if (!model_present[model_idx]) {
                absent_weight_sum += effective_weights[model_idx];
            }
        }
        fused.score =
            fused.score * static_cast<float>(cluster.size()) / (fused.weight + absent_weight_sum);
        return;
    }

    case ConfidenceType::MAX:
        fused.score /= weight_stats.max;
        return;

    case ConfidenceType::AVG:
        if (!allows_overflow) {
            fused.score *= static_cast<float>(std::min(effective_weights.size(), cluster.size())) /
                           weight_stats.sum;
        } else {
            fused.score *= static_cast<float>(cluster.size()) / weight_stats.sum;
        }
        return;
    }
}

auto fuseLabelBoxes(const std::vector<CandidateBox>& boxes, float iou_thr,
                    const std::vector<float>& effective_weights, const WeightStats& weight_stats,
                    ConfidenceType conf_type,
                    bool allows_overflow) // NOLINT(bugprone-easily-swappable-parameters)
    -> std::vector<CandidateBox> {
    std::vector<Cluster> clusters;
    clusters.reserve(boxes.size());

    for (const auto& candidate : boxes) {
        int match_idx = findBestMatchingCluster(clusters, candidate, iou_thr);
        if (match_idx != -1) {
            auto& cluster = clusters[static_cast<std::size_t>(match_idx)];
            cluster.members.push_back(candidate);
            cluster.fused = computeWeightedBox(cluster.members, conf_type);
            continue;
        }
        clusters.push_back(Cluster{
            .members = {candidate},
            .fused = candidate,
        });
    }

    for (auto& cluster : clusters) {
        adjustClusterScore(cluster.fused, cluster.members, effective_weights, weight_stats,
                           conf_type, allows_overflow);
    }

    std::vector<CandidateBox> fused_boxes;
    fused_boxes.reserve(clusters.size());
    for (const auto& cluster : clusters) {
        fused_boxes.push_back(cluster.fused);
    }
    return fused_boxes;
}

auto sortByScoreDesc(std::vector<CandidateBox>& boxes) -> void {
    std::sort(boxes.begin(), boxes.end(),
              [](const CandidateBox& left, const CandidateBox& right) -> bool {
                  return left.score > right.score;
              });
}

} // namespace

auto weightedBoxesFusion(
    const std::vector<ModelBoxes>& boxes_list, const std::vector<ModelScores>& scores_list,
    const std::vector<ModelLabels>& labels_list, const std::vector<float>& weights, float iou_thr,
    bool allows_overflow, float skip_box_thr,
    const std::string& conf_type) // NOLINT(bugprone-easily-swappable-parameters)
    -> std::tuple<ModelBoxes, ModelScores, ModelLabels> {
    if (boxes_list.size() != scores_list.size() || boxes_list.size() != labels_list.size()) {
        throw std::invalid_argument(
            "boxes_list, scores_list, and labels_list must have equal length.");
    }

    std::vector<float> effective_weights = weights;
    if (effective_weights.empty() || effective_weights.size() != boxes_list.size()) {
        effective_weights.assign(boxes_list.size(), 1.0F);
    }

    const ConfidenceType confidence_type = parseConfidenceType(conf_type);

    auto boxes_by_label =
        prefilterBoxes(boxes_list, scores_list, labels_list, effective_weights, skip_box_thr);
    if (boxes_by_label.empty()) {
        return {ModelBoxes{}, ModelScores{}, ModelLabels{}};
    }

    WeightStats weight_stats = computeWeightStats(effective_weights);

    std::vector<CandidateBox> fused_boxes;
    fused_boxes.reserve(default_overall_boxes_reserve);

    for (const auto& [_, boxes] : boxes_by_label) {
        auto fused_label_boxes = fuseLabelBoxes(boxes, iou_thr, effective_weights, weight_stats,
                                                confidence_type, allows_overflow);
        fused_boxes.insert(fused_boxes.end(), fused_label_boxes.begin(), fused_label_boxes.end());
    }

    sortByScoreDesc(fused_boxes);

    ModelBoxes output_boxes;
    ModelScores fused_scores;
    ModelLabels fused_labels;
    output_boxes.reserve(fused_boxes.size());
    fused_scores.reserve(fused_boxes.size());
    fused_labels.reserve(fused_boxes.size());

    for (const auto& candidate : fused_boxes) {
        fused_scores.push_back(candidate.score);
        fused_labels.push_back(candidate.label);
        output_boxes.push_back(
            {candidate.box.x1, candidate.box.y1, candidate.box.x2, candidate.box.y2});
    }

    return {output_boxes, fused_scores, fused_labels};
}

} // namespace nextcv::postprocessing
