// -----------------------------------------------------------------------------
// This file was autogenerated by symforce from template:
//     function/FUNCTION.h.jinja
// Do NOT modify by hand.
// -----------------------------------------------------------------------------

#pragma once

#include <Eigen/Core>

namespace sym {

/**
 * This function was autogenerated from a symbolic function. Do not modify by hand.
 *
 * Symbolic function: compute_airspeed_h_and_k
 *
 * Args:
 *     state: Matrix24_1
 *     P: Matrix23_23
 *     innov_var: Scalar
 *     epsilon: Scalar
 *
 * Outputs:
 *     res0: Matrix23_1
 *     res1: Matrix23_1
 */
template <typename Scalar>
void ComputeAirspeedHAndK(const Eigen::Matrix<Scalar, 24, 1>& state,
                          const Eigen::Matrix<Scalar, 23, 23>& P, const Scalar innov_var,
                          const Scalar epsilon, Eigen::Matrix<Scalar, 23, 1>* const res0 = nullptr,
                          Eigen::Matrix<Scalar, 23, 1>* const res1 = nullptr) {
  // Total ops: 246

  // Input arrays

  // Intermediate terms (7)
  const Scalar _tmp0 = -state(23, 0) + state(5, 0);
  const Scalar _tmp1 = -state(22, 0) + state(4, 0);
  const Scalar _tmp2 = std::pow(Scalar(std::pow(_tmp0, Scalar(2)) + std::pow(_tmp1, Scalar(2)) +
                                       epsilon + std::pow(state(6, 0), Scalar(2))),
                                Scalar(Scalar(-1) / Scalar(2)));
  const Scalar _tmp3 = _tmp1 * _tmp2;
  const Scalar _tmp4 = _tmp0 * _tmp2;
  const Scalar _tmp5 = _tmp2 * state(6, 0);
  const Scalar _tmp6 = Scalar(1.0) / (std::max<Scalar>(epsilon, innov_var));

  // Output terms (2)
  if (res0 != nullptr) {
    Eigen::Matrix<Scalar, 23, 1>& _res0 = (*res0);

    _res0.setZero();

    _res0(3, 0) = _tmp3;
    _res0(4, 0) = _tmp4;
    _res0(5, 0) = _tmp5;
    _res0(21, 0) = -_tmp3;
    _res0(22, 0) = -_tmp4;
  }

  if (res1 != nullptr) {
    Eigen::Matrix<Scalar, 23, 1>& _res1 = (*res1);

    _res1(0, 0) = _tmp6 * (-P(0, 21) * _tmp3 - P(0, 22) * _tmp4 + P(0, 3) * _tmp3 +
                           P(0, 4) * _tmp4 + P(0, 5) * _tmp5);
    _res1(1, 0) = _tmp6 * (-P(1, 21) * _tmp3 - P(1, 22) * _tmp4 + P(1, 3) * _tmp3 +
                           P(1, 4) * _tmp4 + P(1, 5) * _tmp5);
    _res1(2, 0) = _tmp6 * (-P(2, 21) * _tmp3 - P(2, 22) * _tmp4 + P(2, 3) * _tmp3 +
                           P(2, 4) * _tmp4 + P(2, 5) * _tmp5);
    _res1(3, 0) = _tmp6 * (-P(3, 21) * _tmp3 - P(3, 22) * _tmp4 + P(3, 3) * _tmp3 +
                           P(3, 4) * _tmp4 + P(3, 5) * _tmp5);
    _res1(4, 0) = _tmp6 * (-P(4, 21) * _tmp3 - P(4, 22) * _tmp4 + P(4, 3) * _tmp3 +
                           P(4, 4) * _tmp4 + P(4, 5) * _tmp5);
    _res1(5, 0) = _tmp6 * (-P(5, 21) * _tmp3 - P(5, 22) * _tmp4 + P(5, 3) * _tmp3 +
                           P(5, 4) * _tmp4 + P(5, 5) * _tmp5);
    _res1(6, 0) = _tmp6 * (-P(6, 21) * _tmp3 - P(6, 22) * _tmp4 + P(6, 3) * _tmp3 +
                           P(6, 4) * _tmp4 + P(6, 5) * _tmp5);
    _res1(7, 0) = _tmp6 * (-P(7, 21) * _tmp3 - P(7, 22) * _tmp4 + P(7, 3) * _tmp3 +
                           P(7, 4) * _tmp4 + P(7, 5) * _tmp5);
    _res1(8, 0) = _tmp6 * (-P(8, 21) * _tmp3 - P(8, 22) * _tmp4 + P(8, 3) * _tmp3 +
                           P(8, 4) * _tmp4 + P(8, 5) * _tmp5);
    _res1(9, 0) = _tmp6 * (-P(9, 21) * _tmp3 - P(9, 22) * _tmp4 + P(9, 3) * _tmp3 +
                           P(9, 4) * _tmp4 + P(9, 5) * _tmp5);
    _res1(10, 0) = _tmp6 * (-P(10, 21) * _tmp3 - P(10, 22) * _tmp4 + P(10, 3) * _tmp3 +
                            P(10, 4) * _tmp4 + P(10, 5) * _tmp5);
    _res1(11, 0) = _tmp6 * (-P(11, 21) * _tmp3 - P(11, 22) * _tmp4 + P(11, 3) * _tmp3 +
                            P(11, 4) * _tmp4 + P(11, 5) * _tmp5);
    _res1(12, 0) = _tmp6 * (-P(12, 21) * _tmp3 - P(12, 22) * _tmp4 + P(12, 3) * _tmp3 +
                            P(12, 4) * _tmp4 + P(12, 5) * _tmp5);
    _res1(13, 0) = _tmp6 * (-P(13, 21) * _tmp3 - P(13, 22) * _tmp4 + P(13, 3) * _tmp3 +
                            P(13, 4) * _tmp4 + P(13, 5) * _tmp5);
    _res1(14, 0) = _tmp6 * (-P(14, 21) * _tmp3 - P(14, 22) * _tmp4 + P(14, 3) * _tmp3 +
                            P(14, 4) * _tmp4 + P(14, 5) * _tmp5);
    _res1(15, 0) = _tmp6 * (-P(15, 21) * _tmp3 - P(15, 22) * _tmp4 + P(15, 3) * _tmp3 +
                            P(15, 4) * _tmp4 + P(15, 5) * _tmp5);
    _res1(16, 0) = _tmp6 * (-P(16, 21) * _tmp3 - P(16, 22) * _tmp4 + P(16, 3) * _tmp3 +
                            P(16, 4) * _tmp4 + P(16, 5) * _tmp5);
    _res1(17, 0) = _tmp6 * (-P(17, 21) * _tmp3 - P(17, 22) * _tmp4 + P(17, 3) * _tmp3 +
                            P(17, 4) * _tmp4 + P(17, 5) * _tmp5);
    _res1(18, 0) = _tmp6 * (-P(18, 21) * _tmp3 - P(18, 22) * _tmp4 + P(18, 3) * _tmp3 +
                            P(18, 4) * _tmp4 + P(18, 5) * _tmp5);
    _res1(19, 0) = _tmp6 * (-P(19, 21) * _tmp3 - P(19, 22) * _tmp4 + P(19, 3) * _tmp3 +
                            P(19, 4) * _tmp4 + P(19, 5) * _tmp5);
    _res1(20, 0) = _tmp6 * (-P(20, 21) * _tmp3 - P(20, 22) * _tmp4 + P(20, 3) * _tmp3 +
                            P(20, 4) * _tmp4 + P(20, 5) * _tmp5);
    _res1(21, 0) = _tmp6 * (-P(21, 21) * _tmp3 - P(21, 22) * _tmp4 + P(21, 3) * _tmp3 +
                            P(21, 4) * _tmp4 + P(21, 5) * _tmp5);
    _res1(22, 0) = _tmp6 * (-P(22, 21) * _tmp3 - P(22, 22) * _tmp4 + P(22, 3) * _tmp3 +
                            P(22, 4) * _tmp4 + P(22, 5) * _tmp5);
  }
}  // NOLINT(readability/fn_size)

// NOLINTNEXTLINE(readability/fn_size)
}  // namespace sym
