#pragma once
#include <Eigen/Core>
#include <stdexcept>
#include <string>

namespace nextcv::linalg {

// Multiply A (M×N) by x (N) → y (M).
// Using Ref avoids copies and enables zero-copy views from NumPy when contiguous.
auto matvec(const Eigen::Ref<const Eigen::MatrixXf>& A,
            const Eigen::Ref<const Eigen::VectorXf>& x)
    -> Eigen::VectorXf;

}  // namespace nextcv::linalg