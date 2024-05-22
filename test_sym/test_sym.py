

import numpy as np

import symforce

symforce.set_symbolic_api("symengine")
symforce.set_log_level("warning")

# Set epsilon to a symbol for safe code generation.  For more information, see the Epsilon tutorial:
# https://symforce.org/tutorials/epsilon_tutorial.html
symforce.set_epsilon_to_symbol()

import symforce.symbolic as sf
from symforce import codegen
from symforce.codegen import codegen_util
from symforce.notebook_util import display
from symforce.notebook_util import display_code_file
from symforce.values import Values

import shutil


# 1. Define a Python function
def az_el_from_point(
    nav_T_cam: sf.Pose3, nav_t_point: sf.Vector3, epsilon: sf.Scalar = 0
) -> sf.Vector2:
    """
    Transform a nav point into azimuth / elevation angles in the
    camera frame.
    将导航点转换为相机帧中的方位角/仰角

    Args:
        nav_T_cam (sf.Pose3): camera pose in the world
        nav_t_point (sf.Matrix): nav point
        epsilon (Scalar): small number to avoid singularities

    Returns:
        sf.Matrix: (azimuth, elevation)
    """
    # 导航点转换为相机坐标系下的点
    cam_t_point = nav_T_cam.inverse() * nav_t_point
    x, y, z = cam_t_point
    # 根据XY平面的坐标计算方位角
    theta = sf.atan2(y, x + epsilon)
    # 计算仰角: 90度 - 观测点的第三维 z 除以观测点到相机系原点的距离后求反余弦
    phi = sf.pi / 2 - sf.acos(z / (cam_t_point.norm() + epsilon))
    return sf.V2(theta, phi)


# 2. Create a Codegen object using Codegen.function
az_el_codegen = codegen.Codegen.function(
    func=az_el_from_point,
    config=codegen.CppConfig(),
)
# 3. Generate the code
# 由于generate_function没有传递output_dir参赛,因此会在默认目录下生成文件
output_dir="/root/dev/python_ws/test_sym"
az_el_codegen_data = az_el_codegen.generate_function(output_dir)
