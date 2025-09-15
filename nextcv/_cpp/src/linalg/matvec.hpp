#pragma once
#include <Eigen/Core>

namespace nextcv::linalg {

// Multiply matrix (M×N) by vector (N) → y (M).
// Using Ref avoids copies and enables zero-copy views from NumPy when contiguous.
auto matvec(const Eigen::Ref<const Eigen::MatrixXf>& matrix,
            const Eigen::Ref<const Eigen::VectorXf>& vector) -> Eigen::VectorXf;

} // namespace nextcv::linalg
