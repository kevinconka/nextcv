#include "matvec.hpp"

#include <stdexcept>
#include <string>

namespace nextcv::linalg {

// NOLINTNEXTLINE(misc-include-cleaner)
auto matvec(const Eigen::Ref<const Eigen::MatrixXf>& matrix,
            const Eigen::Ref<const Eigen::VectorXf>& vector) -> Eigen::VectorXf {
    if (matrix.cols() != vector.size()) {
        throw std::invalid_argument(
            "matvec: shape mismatch: matrix is " + std::to_string(matrix.rows()) + "x" +
            std::to_string(matrix.cols()) + ", vector is " + std::to_string(vector.size()));
    }
    return matrix * vector; // Eigen handles allocation and optimized kernel
}

} // namespace nextcv::linalg
