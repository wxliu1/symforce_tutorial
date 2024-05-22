
"""
One of the most important features of symforce is the ability to generate computationally efficient code from symbolic expressions. 
symforce最重要的特征之一是能够从符号表达式生成计算效率高的代码。

The typical workflow for generating a function is to define a Python function that operates on symbolic inputs to return the symbolic result. Typically this will look like:
生成函数的典型工作流是定义一个对符号输入进行操作的python函数来返回符号结果。

1. Define a Python function that operates on symbolic inputs

2. Create a Codegen object using Codegen.function. Various properties of the function will be deduced automatically; for instance, the name of the generated function is generated from the name of the Python function, and the argument names and types are deduced from the Python function argument names and type annotations.

3. Generate the code in your desired language
"""

"""
Alternately, you may want to define the input and output symbolic Values explicitly, with the following steps:

1. Build an input Values object that defines a symbolic representation of each input to the function. Note that inputs and outputs can be Values objects themselves, which symforce will automatically generate into custom types.

2. Build an output Values object that defines the outputs of the function in terms of the objects in the input Values.

3. Generate the code in your desired language
"""



# Setup
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



"""
Generating from a Python function
First, we look at using existing python functions to generate an equivalent function using the codegen package. The inputs to the function are automatically deduced from the signature and type annotations. Additionally, we can change how the generated function is declared (e.g. whether to return an object using a return statement or a pointer passed as an argument to the function).
"""

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
az_el_codegen_data = az_el_codegen.generate_function()
# az_el_codegen_data.output_dir存储的是生成文件的目录的前两级
print("Files generated in {}:\n".format(az_el_codegen_data.output_dir))
for f in az_el_codegen_data.generated_files:
    # 打印完整目录关于前两级目录之后的部分
    print("  |- {}".format(f.relative_to(az_el_codegen_data.output_dir)))

# az_el_codegen_data.generated_files[0]存储的是生成文件的完整目录
print(az_el_codegen_data.generated_files[0])
# 根据生成后的cpp文件完整路径，输出转换后的代码
print_code: bool = False
if print_code:
    display_code_file(az_el_codegen_data.generated_files[0], "C++")

output_dir = None
# 如果输出目录为空，则删除生成的文件
if output_dir is None:
        shutil.rmtree(az_el_codegen_data.output_dir)





# Generating function jacobians
# 分别求方位角、仰角关于位姿、导航点的雅可比
codegen_with_jacobians = az_el_codegen.with_jacobians(
    # Just compute wrt the pose and point, not epsilon
    which_args=["nav_T_cam", "nav_t_point"],
    # Include value, not just jacobians
    include_results=True,
)

data = codegen_with_jacobians.generate_function()
if False:
    display_code_file(data.generated_files[0], "C++")
# 删除生成的文件的所在目录
shutil.rmtree(data.output_dir)




"""
Code generation using implicit functions
Next, we look at generating functions using a list of input variables and output expressions that are a function of those variables. In this case we don’t need to explicitly define a function in python, but can instead generate one directly using the codegen package.
接下来，我们将使用输入变量和这些变量的输出表达式列表来研究生成函数。在这种情况下，我们不需要在python中显式地定义一个函数，而是可以直接使用codegen包生成一个函数。 

Let’s set up an example for the double pendulum. We’ll skip the derivation and just define the equations of motion for the angular acceleration of the two links:
"""

# Define symbols
L = sf.V2.symbolic("L").T  # Length of the two links
m = sf.V2.symbolic("m").T  # Mass of the two links
ang = sf.V2.symbolic("a").T  # Angle of the two links
dang = sf.V2.symbolic("da").T  # Angular velocity of the two links
g = sf.Symbol("g")  # Gravity

# Angular acceleration of the first link
ddang_0 = (
    -g * (2 * m[0] + m[1]) * sf.sin(ang[0])
    - m[1] * g * sf.sin(ang[0] - 2 * ang[1])
    - 2
    * sf.sin(ang[0] - ang[1])
    * m[1]
    * (dang[1] * 2 * L[1] + dang[0] * 2 * L[0] * sf.cos(ang[0] - ang[1]))
) / (L[0] * (2 * m[0] + m[1] - m[1] * sf.cos(2 * ang[0] - 2 * ang[1])))
display(ddang_0)

# Angular acceleration of the second link
ddang_1 = (
    2
    * sf.sin(ang[0] - ang[1])
    * (
        dang[0] ** 2 * L[0] * (m[0] + m[1])
        + g * (m[0] + m[1]) * sf.cos(ang[0])
        + dang[1] ** 2 * L[1] * m[1] * sf.cos(ang[0] - ang[1])
    )
) / (L[1] * (2 * m[0] + m[1] - m[1] * sf.cos(2 * ang[0] - 2 * ang[1])))
display(ddang_1)

# Now let’s organize the input symbols into a Values hierarchy:
inputs = Values()

inputs["ang"] = ang
inputs["dang"] = dang

with inputs.scope("constants"):
    inputs["g"] = g

with inputs.scope("params"):
    inputs["L"] = L
    inputs["m"] = m

display(inputs)

# The output will simply be a 2-vector of the angular accelerations:
outputs = Values(ddang=sf.V2(ddang_0, ddang_1))

display(outputs)

# Now run code generation to produce an executable module (in a temp directory if none provided):
double_pendulum = codegen.Codegen(
    inputs=inputs,
    outputs=outputs,
    config=codegen.CppConfig(),
    name="double_pendulum",
    return_key="ddang", # 指定返回参数
)
double_pendulum_data = double_pendulum.generate_function()

# Print what we generated
print("Files generated in {}:\n".format(double_pendulum_data.output_dir))
for f in double_pendulum_data.generated_files:
    print("  |- {}".format(f.relative_to(double_pendulum_data.output_dir)))

# 显示/tmp/sf_codegen_double_pendulum_m29dfluw/cpp/symforce/sym
display(double_pendulum_data.function_dir)
if False:
    display_code_file(double_pendulum_data.function_dir / "double_pendulum.h", "C++")
if True:
    shutil.rmtree(double_pendulum_data.output_dir)    


#display(inputs)
#display(outputs)


# We can also generate functions with different function declarations:
# 我们还可以生成具有不同函数声明的函数

# Function using structs as inputs and outputs (returned as pointer arg)
# 函数用结构体作为输入和输出(输出作为指针参数返回)
# 这里似乎是把Values类型的inputs和outputs再一次封装构造成Values对象的值，在生成代码时就可以变成结构体
input_values = Values(inputs=inputs)
output_values = Values(outputs=outputs)
#display(input_values)
#display(output_values)
namespace = "double_pendulum"
double_pendulum_values = codegen.Codegen(
    inputs=input_values,
    outputs=output_values,
    config=codegen.CppConfig(),
    name="double_pendulum", # 指定函数名称
)
double_pendulum_values_data = double_pendulum_values.generate_function(
    namespace=namespace, # 指定命名空间
)

# Print what we generated. Note the nested structs that were automatically
# generated.
print("Files generated in {}:\n".format(double_pendulum_values_data.output_dir))
for f in double_pendulum_values_data.generated_files:
    print("  |- {}".format(f.relative_to(double_pendulum_values_data.output_dir)))

display_code_file(
    double_pendulum_values_data.function_dir / "double_pendulum.h",
    "C++",
)

if True:
    shutil.rmtree(double_pendulum_values_data.output_dir)




# Finally, we can generate the same function in other languages as well:
# 生成python语言的函数
namespace = "double_pendulum"
double_pendulum_python = codegen.Codegen(
    inputs=inputs,
    outputs=outputs,
    config=codegen.PythonConfig(use_eigen_types=False),
    name="double_pendulum",
    return_key="ddang",
)
double_pendulum_python_data = double_pendulum_python.generate_function(
    namespace=namespace,
)

print("Files generated in {}:\n".format(double_pendulum_python_data.output_dir))
for f in double_pendulum_python_data.generated_files:
    print("  |- {}".format(f.relative_to(double_pendulum_python_data.output_dir)))

display_code_file(
    double_pendulum_python_data.function_dir / "double_pendulum.py",
    "python",
)


# 调用生成的python函数接口
constants_t = codegen_util.load_generated_lcmtype(
    namespace, "constants_t", double_pendulum_python_data.python_types_dir
)

params_t = codegen_util.load_generated_lcmtype(
    namespace, "params_t", double_pendulum_python_data.python_types_dir
)

ang = np.array([[0.0, 0.5]])
dang = np.array([[0.0, 0.0]])
consts = constants_t()
consts.g = 9.81
params = params_t()
params.L = [0.5, 0.3]
params.m = [0.3, 0.2]

gen_module = codegen_util.load_generated_package(
    namespace, double_pendulum_python_data.function_dir
)
dddang=gen_module.double_pendulum(ang, dang, consts, params)
print(dddang)

if True:
    shutil.rmtree(double_pendulum_python_data.output_dir)    
