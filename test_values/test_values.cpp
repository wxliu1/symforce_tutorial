
#include <symforce/opt/values.h>
#include <iostream>

/**
 * 
 * 关于sym::Values类：
 * 要求实现了StorageOps和LieGroupOps，才能兼容
 * 
 * Compatible types are given by the type_t enum. All types implement the StorageOps and
 * LieGroupOps concepts, which are the core operating mechanisms in this class.
 *
 * 基本上需要支持以下的一些操作
 * Ops Tutorial：
 * StorageOps: Data type that can be serialized to and from a vector of scalar quantities.
 * GroupOps: Mathematical group that implements closure, associativity, identity and invertibility.
 * LieGroupOps: Group that is also a differentiable manifold, such that calculus applies.
 * 
 */

template <typename ScalarType>
struct MyStruct
{
    using Scalar = ScalarType;
    using Self = MyStruct<Scalar>;
    using DataVec = Eigen::Matrix<Scalar, 4, 1>;
    // double para_Pose[7];
    Scalar para_Pose[7];

    DataVec data;
/*
    static constexpr int32_t StorageDim() {
        return sym::StorageOps<Self>::StorageDim();
    }

    void ToStorage(Scalar* const vec) const {
        return sym::StorageOps<Self>::ToStorage(*this, vec);
    }

    static MyStruct FromStorage(const Scalar* const vec) {
        return sym::StorageOps<Self>::FromStorage(vec);
    }*/
};

int main(int argc, char** argv)
{
    sym::Values<double> values;
    values.Set({'P', 0}, sym::Pose2d::Identity());
    values.Set({'L', 0}, Eigen::Vector2d(-2, 2));
    // values.Set('a', 10); // error
    // values.Set({'a'}, 10.0); // ok
    values.Set('a', 10.0); // ok
    values.Set({'d', 0}, 1.7);
    values.Set('e', sym::kDefaultEpsilond);

    double pi = 3.1415926;
    double* pPi = &pi;
    // values.Set('x', pi); //ok
    // values.Set('x', pPi); // error
    // values.Set('x', "abc"); // error
    std::cout << "'x'=" << values.At<double>('x') << std::endl;

    // values.Set('y', 10); // error
    // std::cout << "'y'=" << values.At<int>('y') << std::endl; // error

/*
    std::cout << "{'P', 0}=" << values.At<sym::Pose2d>({'P', 0}) << std::endl;
    std::cout << "{'L', 0}=" << values.At<Eigen::Vector2d>({'L', 0}).transpose() << std::endl;
    std::cout << "'a'=" << values.At<double>('a') << std::endl;
    std::cout << "'e'=" << values.At<double>('e') << std::endl;
    std::cout << "{'d', 0}=" << values.At<double>({'d', 0}) << std::endl;
    // std::cout << "{'d', 0}=" << values.At<float>({'d', 0}) << std::endl;

    std::cout << values << std::endl;
*/

    Eigen::MatrixXd linearized_jacobians;
    Eigen::VectorXd linearized_residuals;

    // sym::Values<double *> values2; // error
    sym::Values<float> values22;
    // sym::Values<int> values23;
    sym::Values<double> values2;
    // linearized_jacobians = Eigen::Matrix<double, 4, 5>::Random();
    linearized_jacobians = Eigen::Matrix<double, 75, 75>::Random();
    // std::cout << linearized_jacobians << std::endl;
    const int rows = linearized_jacobians.rows();
    const int cols = linearized_jacobians.cols();
    std::cout << "rows=" << rows << " cols=" << cols << std::endl;
    // values2.Set('m', Eigen::Matrix<double, rows, cols>(linearized_jacobians)); // error
    // values2.Set('m', Eigen::Matrix<double, 4, 5>(linearized_jacobians)); // ok
    values2.Set('m', Eigen::Matrix<double, 75, 75>(linearized_jacobians)); // ok
    // values2.Set('m', linearized_jacobians); // error


    // std::cout << "'m'=" << values2.At<Eigen::MatrixXd>('m') << std::endl; // error
    // std::cout << "'m'=" << values2.At('m') << std::endl; // error
    // std::cout << "'m'=" << values2.At<Eigen::Matrix<double, 4, 5>>('m') << std::endl; // ok
    // std::cout << "'m'=" << values2.At<Eigen::Matrix<double, 75, 75>>('m') << std::endl; // ok

/*
 * test ok
    Eigen::Matrix<double, 4, 5> tmp_matrix = Eigen::Matrix<double, 4, 5>::Random();
    Eigen::Matrix<double, 3, 1> tmp_matrix2 = Eigen::Matrix<double, 3, 1>::Random();
    // values2.Set('t', Eigen::Matrix<double, 4, 5>(tmp_matrix));
    values2.Set({'t'}, tmp_matrix);
    std::cout << "'t'=" << values2.At<Eigen::Matrix<double, 4, 5>>({'t'}) << std::endl;

    values2.Set('r', tmp_matrix2);
    std::cout << "'r'=" << values2.At<Eigen::Matrix<double, 3, 1>>({'r'}) << std::endl;

    Eigen::Vector2d source_uv;
    values2.Set({'v', 1}, source_uv);
    // std::cout << "{'v', 1}=" << values.At<Eigen::Vector2d>({'v', 1}) << std::endl;
    std::cout << "{'v', 1}=" << values2.At<Eigen::Vector2d>({'v', 1}) << std::endl;
*/

    MyStruct<double> mys;
    // values2.Set('s', mys);
    // values2.Set({'s', 0}, mys);



    // values2.Set('a', 10);

    // sym::Values<MyStruct> values2;

    

    // double para_Pose[10 + 1][7];
    // int i = 0;
    // for(i = 0; i <= 10; i++)
    // {
    //     values.Set({'P', i}, reinterpret_cast<long>(para_Pose[i]));
    // }

    return 0;
}