#include "nms.hpp"
#include <Eigen/src/Core/Matrix.h>
#include <algorithm>
#include <cstddef>
#include <numeric>
#include <vector>

namespace nextcv::postprocessing {

auto nms(const Eigen::MatrixXf& bboxes, const Eigen::VectorXf& scores,
         float threshold) // NOLINT(bugprone-easily-swappable-parameters)
    -> std::vector<int> {
    if (bboxes.rows() == 0) {
        return {};
    }

    // Areas of bboxes
    Eigen::VectorXf areas =
        (bboxes.col(2) - bboxes.col(0)).cwiseProduct(bboxes.col(3) - bboxes.col(1));

    // Sort by scores
    std::vector<int> indices(static_cast<std::size_t>(scores.size()));
    std::iota(indices.begin(), indices.end(), 0);
    std::sort(indices.begin(), indices.end(),
              [&](int i, int j) -> bool { return scores(i) > scores(j); });

    std::vector<int> keep;
    std::vector<bool> is_suppressed(static_cast<std::size_t>(scores.size()), false);

    for (int i = 0; i < static_cast<int>(scores.size()); ++i) {
        int idx = indices[static_cast<std::size_t>(i)];
        if (is_suppressed[static_cast<std::size_t>(idx)]) {
            continue;
        }
        keep.push_back(idx);

        for (int j = i + 1; j < static_cast<int>(scores.size()); ++j) {
            int other_idx = indices[static_cast<std::size_t>(j)];
            if (is_suppressed[static_cast<std::size_t>(other_idx)]) {
                continue;
            }

            // Intersection
            float ix1 = std::max(bboxes(idx, 0), bboxes(other_idx, 0));
            float iy1 = std::max(bboxes(idx, 1), bboxes(other_idx, 1));
            float ix2 = std::min(bboxes(idx, 2), bboxes(other_idx, 2));
            float iy2 = std::min(bboxes(idx, 3), bboxes(other_idx, 3));

            float inter_area = std::max(0.0F, ix2 - ix1) * std::max(0.0F, iy2 - iy1);

            // Union
            float union_area = areas(idx) + areas(other_idx) - inter_area;

            // IoU
            float iou = inter_area / union_area;

            if (iou > threshold) {
                is_suppressed[static_cast<std::size_t>(other_idx)] = true;
            }
        }
    }
    return keep;
}

} // namespace nextcv::postprocessing
