
#include <sym/posed_camera.h>
#include<iostream>

int main(int argc, char* argv[])
{
    std::cout << sym::Pose3d() << std::endl;
    std::cout << sym::Rot3<double>() << std::endl;

    sym::Rot3<double> Q = sym::Rot3<double>();
    const Eigen::Matrix<double, 4, 1>& rotation = Q.Data();
    std::cout << "rotation=" << rotation.transpose() << std::endl;

    // seems to no sym::Quaternion<double>()
    // std::cout << "sym::Quaternion<double>()=" << sym::Quaternion<double>() << std::endl; // error

    return 0;
}