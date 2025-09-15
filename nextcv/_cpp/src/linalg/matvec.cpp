#include "matvec.hpp"

namespace nextcv::linalg {

auto matvec(const Eigen::Ref<const Eigen::MatrixXf>& A,
            const Eigen::Ref<const Eigen::VectorXf>& x) -> Eigen::VectorXf {
  if (A.cols() != x.size()) {
    throw std::invalid_argument(
        "matvec: shape mismatch: A is " + std::to_string(A.rows()) + "x" +
        std::to_string(A.cols()) + ", x is " + std::to_string(x.size()));
  }
  return A * x;  // Eigen handles allocation and optimized kernel
}

}  // namespace nextcv::linalg