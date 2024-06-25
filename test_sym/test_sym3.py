import symforce
symforce.set_epsilon_to_symbol()

from symforce import codegen
from symforce.codegen import codegen_util

import symforce.symbolic as sf
from symforce.notebook_util import display

point = sf.V3.symbolic("p")
display(point)
display(point[:2])
string = "abcdefg"
display(string[:2])
display(string[3:])

# residual = sf.V15.symbolic("r") # error
# m = sf.Matrix.ones(15, 1)
m = sf.Matrix52.symbolic("m")
# display(residual)
display(m)

def generate_matrix() -> sf.Matrix:
    return sf.Matrix.zeros(15, 1)

residual = generate_matrix()
# display(residual)

world_T_body = sf.Pose3.symbolic("T")
display(world_T_body)
# display(sf.Rot3.symbolic("R"))

# display(sf.Quaternion.symbolic("q"))

# display(sf.Rot3())

# display(sf.Vector6.symbolic("r"))

R = sf.Rot3.symbolic("R")
# display(R.inverse())
# display(R.inverse() * R)
# display(R * R.inverse())

R1 = sf.Rot3.random()
R1_inv = R1.inverse()
# display(R1)
# display(R1_inv * R1)


R2 = sf.Quaternion.symbolic("q")
display(R2.xyz)
R2_inv = R2.inverse()
# display(R2)
# display(R2_inv * R2)

m9 = sf.Matrix23.block_matrix([[sf.M13([1, 2, 3])], [sf.M13([3, 4, 5])]])
print(m9)

m2 = sf.Matrix(2, 3, [1, 2, 3, 4, 5, 6])
print(m2)

v3 = sf.Matrix31(1, 2, 3)
v4 = sf.M31(1, 2, 3)
v5 = sf.Vector3(1, 2, 3)
v6 = sf.V3(1, 2, 3)
print(f"v6.rows={v6.rows}, v6.cols={v6.cols}")

# For example:

# [[Matrix22(...), Matrix23(...)], [Matrix11(...), Matrix14(...)]]
# constructs a Matrix35 with elements equal to given blocks

mm = sf.Matrix([v3.to_storage(), v4.to_storage(), v5.to_storage(), v6.to_storage()]) 
print(mm)
print(mm.rows)
print(mm.cols)

mm2 = sf.Matrix.block_matrix([[v3], [v4], [v5], [v6]])
print(mm2)
print(f"mm2.rows={mm2.rows}, mm2.cols={mm2.cols}")


mm3 = sf.Matrix.block_matrix([[v3, v4], [v5, v6]])
print(mm3)
print(f"mm3.rows={mm3.rows}, mm3.cols={mm3.cols}") # 6 * 2

residual2 = sf.Matrix(6, 1)
display(residual2)
display(residual2.T)

display(residual2.rows)
display(residual2.T.rows)

from symforce.ops import StorageOps
display(StorageOps.storage_dim(residual2))

mystr="aaa"
def myfunc():
    print(mystr)

myfunc()

vv = sf.V3(1, 2, 3)
print(vv.y)
print(vv.z)

r_x = 3
r_y = 1
rrr = sf.V2(r_x, r_y)
print(rrr)

o1 = sf.Matrix23.one()
o2 = sf.Matrix.ones(2, 3)
display(o1)
display(o2)
display(sf.I22(2, 2))
display(sf.I2(2, 2))
display(sf.I22(2))

identity_matrix = sf.Matrix33.eye()
print(identity_matrix)

# identity_matrix2 = sf.Matrix33.I3() # error
# print(identity_matrix2)


# display(epsilon)

# epsilon: sf.Scalar
# display(lambda s: 1 / (s + epsilon))

epsilon = 0.001
epsilon=sf.numeric_epsilon
display(f"epsilon={epsilon}")

lambda s: 1 / (s + epsilon)
func = lambda s: 1 / (s + epsilon)
display(func(2))

display(sf.V2(0, 0))

# max2函数包含分支，这样符号化之后的函数不会有正确的结果
def max2(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    # if a > b:
    #     retval = a #f"a > b"
    # else:
    #     retval = b #f"a < b"
    retval = a if a > b else b
    return retval
 
print(max2(5,4))

max2_codegen = codegen.Codegen.function(
    func=max2,
    config=codegen.CppConfig(),
)
    
output_dir="/root/dev/python_ws/test_sym"
# max2_data = max2_codegen.generate_function(output_dir)



yaw_diff = sf.Symbol("y")
display(sf.sin(yaw_diff))

m3 = sf.Matrix33(1, 2, 3, 4, 5, 6, 7, 8, 9)
display(m3)

sin_yaw_diff = sf.sin(yaw_diff)
cos_yaw_diff = sf.cos(yaw_diff)
R_enu_local = sf.Matrix33(cos_yaw_diff, -sin_yaw_diff, 0, \
                          sin_yaw_diff, cos_yaw_diff, 0, \
                          0, 0, 1)

display(R_enu_local)
display(sf.V3.zero())

xyz = sf.V3.symbolic("xyz")
display(xyz.z)

a = sf.Symbol("a")
b = sf.Symbol("b")
c = sf.Pow(a, b)
print(c)
display(a**b)
display(4 ** 3)

display(sf.Max(a, b))
retval = b + sf.Max(sf.sign(a - b), 0) * (a - b)
display(retval)

from symengine import atan
display(atan(sf.Symbol("x")))
display(atan(1))

display(sf.epsilon())

display(sf.sign(6))
display(sf.sign(-3))
display(sf.sign(0))

display(sf.Max(1, 0))

def max3(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    # retval = a + sf.Max(sf.sign(a - b), 0)(b - a)
    # retval = b + sf.Max(sf.sign(a - b), 0)(a - b)
    retval = sf.Max(a, b)
    # retval = sf.sign(a - b)

    return retval


print(f"max3(-5,4)={max3(-5,4)}")

max3_codegen = codegen.Codegen.function(
    func=max3,
    config=codegen.CppConfig(),
)
# max3_data = max3_codegen.generate_function(output_dir)


def max4(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    # retval = a + sf.Max(sf.sign(a - b), 0)(b - a)
    # 很好的一个改进条件表达式的方法
    retval = b + sf.Max(sf.sign(a - b), 0) * (a - b)
    # retval = sf.Max(a, b)

    return retval


print(f"max4(-5, -4)={max4(-5,-4)}")

max4_codegen = codegen.Codegen.function(
    func=max4,
    config=codegen.CppConfig(),
)
max4_data = max4_codegen.generate_function(output_dir)



def max5(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    if(a > b): return a#retval

    retval = a + b

    return retval


print(f"max5(-5, -4)={max5(-5,-4)}")
print(f"max5(-5, -14)={max5(-5,-14)}")

max5_codegen = codegen.Codegen.function(
    func=max5,
    config=codegen.CppConfig(),
)
max5_data = max5_codegen.generate_function(output_dir)