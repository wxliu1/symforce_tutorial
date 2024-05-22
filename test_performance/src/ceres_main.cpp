
#include "robot_3d_localization_ceres.h"

#include <symforce/opt/factor.h>
#include <symforce/opt/optimizer.h>
#include <symforce/opt/tic_toc.h>

#include <chrono>

using namespace robot_3d_localization;

int main(int argc, char** argv)
{

    auto problem_and_vars = BuildCeresProblem();
    auto& problem = std::get<0>(problem_and_vars);
    auto& rotations = std::get<1>(problem_and_vars);
    auto& positions = std::get<2>(problem_and_vars);

    ceres::Solver::Options options;
    options.max_num_iterations = 200; // 8
    options.function_tolerance = 1e-15;
    options.parameter_tolerance = 1e-30;
    options.linear_solver_type = ceres::SPARSE_NORMAL_CHOLESKY;
    options.logging_type = ceres::SILENT;

    ceres::Solver::Summary summary;

    // Solve - further solves should terminate in 1 iteration
    auto start = std::chrono::steady_clock::now();
    ceres::Solve(options, &problem, &summary);
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> diff = end - start;

    std::cout << std::fixed << " solve time cost : " << diff.count() << " s\n";
    // std::cout << "Iterations: " << summary.iterations.size() << std::endl;

    std::cout << summary.BriefReport() << std::endl;

    for (int i = 0; i < kNumPoses; ++i) {
        // 输出系数q.coeffs().transpose(); //[x y z w]
        // 输出虚部q.vec(); //[x y z]
        //cout<<q.w()<<" “<<q.x()<<” “<<q.y()<<” "<<q.z()<<endl;
        std::cout << "q=" << rotations[i].coeffs().transpose();// << std::endl;
        std::cout << " t=" << positions[i].transpose() << std::endl;
    }
/*
    std::chrono::milliseconds timespan(100);
    std::this_thread::sleep_for(timespan);

    {
        SYM_TIME_SCOPE("ceres_dynamic_d/iterate");
        for (int i = 0; i < 1000; ++i) {
        ceres::Solve(options, &problem, &summary);
        }
    }
*/
    return 0;
}