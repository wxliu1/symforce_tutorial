
import symforce

symforce.set_epsilon_to_symbol()

from symforce import path_util
from symforce.examples.robot_2d_localization import robot_2d_localization
from symforce.test_util import TestCase
from symforce.test_util import symengine_only

BASE_DIRNAME = "symforce_robot_2d_localization_example"


output_dir="/root/dev/python_ws/test_robot_2d_localization"
#robot_2d_localization.generate_bearing_residual_code(output_dir)
#robot_2d_localization.generate_odometry_residual_code(output_dir)

robot_2d_localization.generate_bearing_residual_code(output_dir=output_dir)
robot_2d_localization.generate_odometry_residual_code(output_dir=output_dir)
