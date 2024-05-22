# Setup
import symforce

symforce.set_symbolic_api("sympy")
symforce.set_log_level("warning")

import symforce.symbolic as sf
from symforce import ops
from symforce.notebook_util import display

"""
Rotations can be defined from and converted to a number of different representations as shown below, but always use a quaternion as the underlying representation. We use the notation world_R_body to represent a rotation that rotates a point written in the body frame into the world frame.

Note that in some cases a small epsilon can be provided to prevent numerical errors (e.g. division by zero) when converting to/from rotation representations. Furthermore, converting between certain representations can require additional symbolic expressions to guard against degenerate cases. For example, a rotation constructed from a rotation matrix results in more complexity than when constructed using an axis-angle representation as shown below.
"""

# Identity definition
display(sf.Rot3())


# Symbolic definition
display(sf.Rot3.symbolic("R"))


# From a quaternion of the form qw + qv0 + qv1 + qv2
qv = sf.V3.symbolic("qv")
qw = sf.Symbol("qw")
quat = sf.Quaternion(xyz=qv, w=qw)
display(quat)
# we can use this quaternion to initialize a sf.Rot3:
R_from_quat = sf.Rot3(quat)
display(R_from_quat)


# To/From rotation matrix

# Rotate about x-axis
theta = sf.Symbol("theta")
R_mat = sf.Matrix(
    [
        [1, 0, 0],
        [0, sf.cos(theta), -sf.sin(theta)],
        [0, sf.sin(theta), sf.cos(theta)],
    ]
)
# 从旋转矩阵构建四元数，得到的四元数超级复杂
R = sf.Rot3.from_rotation_matrix(R_mat)

display(R_mat)
'''
display(R)  # Note the additional expressions required to avoid numerical errors
display(R.to_rotation_matrix()) # 从四元数转换到旋转矩阵也超级复杂
'''


# To/From Euler angles
R = sf.Rot3.from_yaw_pitch_roll(0, 0, theta)  # Yaw rotation only
ypr = R.to_yaw_pitch_roll()

display(R)
display(ops.StorageOps.simplify(list(ypr)))  # Simplify YPR expression


# From axis-angle representation

# Rotate about x-axis
R = sf.Rot3.from_angle_axis(angle=theta, axis=sf.Vector3(1, 0, 0))

display(R)



# Rotation defining orientation of body frame wrt world frame
world_R_body = sf.Rot3.symbolic("R")

# Point written in body frame
body_t_point = sf.Vector3.symbolic("p")

# Point written in world frame
world_t_point = world_R_body * body_t_point

display(world_t_point)




body_R_cam = sf.Rot3.symbolic("R_cam")
world_R_cam = world_R_body * body_R_cam

# Rotation inverse = negate vector part of quaternion
cam_R_body = body_R_cam.inverse()
display(body_R_cam)
display(cam_R_body)
"""
output:
<Rot3 <Q xyzw=[R_cam_x, R_cam_y, R_cam_z, R_cam_w]>>
<Rot3 <Q xyzw=[-R_cam_x, -R_cam_y, -R_cam_z, R_cam_w]>>
"""

'''
We can also easily substitute numerical values into symbolic expressions using geo objects themselves. This makes it very convenient to substitute numeric values into large symbolic expressions constructed using many different geo objects.
'''
world_R_body_numeric = sf.Rot3.from_yaw_pitch_roll(0.1, -2.3, 0.7)
display(world_t_point.subs(world_R_body, world_R_body_numeric))




"""
Poses
Poses are defined as a rotation plus a translation, and are constructed as such. We use the notation world_T_body to represent a pose that transforms from the body frame to the world frame.
"""

# Symbolic construction
world_T_body = sf.Pose3.symbolic("T")
display(world_T_body)


# Construction from a rotation and translation

# Orientation of body frame wrt world frame
world_R_body = sf.Rot3.symbolic("R")

# Position of body frame wrt world frame written in the world frame
world_t_body = sf.Vector3.symbolic("t")

world_T_body = sf.Pose3(R=world_R_body, t=world_t_body)
display(world_T_body)



# Compose pose with a pose
body_T_cam = sf.Pose3.symbolic("T_cam")
world_T_cam = world_T_body * body_T_cam

# Compose pose with a point
body_t_point = sf.Vector3.symbolic("p")  # Position in body frame
# Equivalent to: world_R_body * body_t_point + world_t_body
world_t_point = world_T_body * body_t_point
display(world_t_point)


# Invert a pose
body_T_world = world_T_body.inverse()
display(world_T_body)
display(body_T_world)



"""
Vectors and matrices are all represented using subclasses of sf.Matrix class, and can be constructed in several different ways as shown below.
"""

# Matrix construction. The statements below all create the same 2x3 matrix object

# Construction from 2D list
m1 = sf.Matrix([[1, 2, 3], [4, 5, 6]])

# Construction using specified size + data
m2 = sf.Matrix(2, 3, [1, 2, 3, 4, 5, 6])

# sf.MatrixNM creates a matrix with shape NxM (defined by default for 6x6
# matrices and smaller)
m3 = sf.Matrix23(1, 2, 3, 4, 5, 6)
m4 = sf.Matrix23([1, 2, 3, 4, 5, 6])

# Construction using aliases
m5 = sf.M([[1, 2, 3], [4, 5, 6]])
m6 = sf.M(2, 3, [1, 2, 3, 4, 5, 6])
m7 = sf.M23(1, 2, 3, 4, 5, 6)
m8 = sf.M23([1, 2, 3, 4, 5, 6])

# Construction from block matrices of appropriate dimensions
m9 = sf.Matrix23.block_matrix([[sf.M13([1, 2, 3])], [sf.M13([3, 4, 5])]])
print(m9)



# Vector constructors. The statements below all create the same 3x1 vector object

# Construction from 2D list
v1 = sf.Matrix([[1], [2], [3]])
print(v1)

# Construction from 1D list. We assume a 1D list represents a column vector.
v2 = sf.Matrix([1, 2, 3])
print(v2)

# Construction using aliases (defined by default for 9x1 vectors and smaller)
v3 = sf.Matrix31(1, 2, 3)
v4 = sf.M31(1, 2, 3)
v5 = sf.Vector3(1, 2, 3)
v6 = sf.V3(1, 2, 3)



# Matrix of zeros
z1 = sf.Matrix23.zero()
z2 = sf.Matrix.zeros(2, 3)

# Matrix of ones
o1 = sf.Matrix23.one()
o2 = sf.Matrix.ones(2, 3)



"""
Note that the Matrix class itself does not contain group or lie group methods, to prevent confusion between the identity matrix and inverse matrix, and the group operations under addition. The group operations are implemented separately for matrices under addition, and are accessed through ops.GroupOps and ops.LieGroupOps.
"""

zero_matrix = sf.Matrix33.zero()
identity_matrix = sf.Matrix33.eye()

# We could also write:
zero_matrix = ops.GroupOps.identity(sf.Matrix33)

display(zero_matrix)
display(identity_matrix)


# Matrix multiplication
m23 = sf.M23.symbolic("lhs")
m31 = sf.V3.symbolic("rhs")
display(m23 * m31)


# Vector operations
norm = m31.norm()
display(norm)
squared_norm = m31.squared_norm()
unit_vec = m31.normalized()
display(unit_vec)


m33 = 5 * sf.Matrix33.eye()  # Element-wise multiplication with scalar
display(m33.inv())  # Matrix inverse


'''
One of the most powerful operations we can use matrices for is to compute jacobians with respect to other geo objects. By default we compute jacobians with respect to the tangent space of the given object.
'''

R0 = sf.Rot3.symbolic("R0")
R1 = sf.Rot3.symbolic("R1")
print(R0)

residual = sf.M(R0.local_coordinates(R1))
display(residual)
display(residual.shape)
display(R0.storage_dim())
# quit(0)


jacobian = residual.jacobian(R1)
# The jacobian is quite a complex symbolic expression, so we don't display it for
# convenience.
# The shape is equal to (dimension of residual) x (dimension of tangent space)
display(jacobian.shape)



"""
General properties of geo objects
Storage operations
All geometric types implement the “Storage” interface. This means that they can:

Be serialized into a list of scalar expressions (.to_storage())

Be reconstructed from a list of scalar expressions (.from_storage())

Use common symbolic operations (symbolic construction, substitution, simplification, etc.)
"""
'''
所有的几何类型都实现了“存储”接口。这意味着他们可以：
被序列化为一个标量表达式列表(.to_storage())
从一系列标量表达式中重建(.from_storage())
使用常用的符号操作(符号构造、替换、简化等)
'''

# Serialization to scalar list
rot = sf.Rot3()
elements = rot.to_storage()
assert len(elements) == rot.storage_dim()
display(elements)


# Construction from scalar list
rot2 = sf.Rot3.from_storage(elements)
assert rot == rot2


# Symbolic operations
rot_sym = sf.Rot3.symbolic("rot_sym")
# 符号表达式的替换操作，将符号rot_sym替换为值rot
rot_num = rot_sym.subs(rot_sym, rot)

display(rot_sym)
display(rot_num)
display(rot_num.simplify())  # Simplify internal symbolic expressions
display(rot_num.evalf())  # Numerical evaluation



"""
Group operations
All geometric types also implement the “Group” interface, meaning that geometric objects:

Can be composed with objects of the same type to produce an object of the same type (.compose())

Have an identity element (.identity())

Can be inverted (.inverse())

Can be created to represent the relation between two other objects of the same type (.between())
"""



# Construct two random rotations
R1 = sf.Rot3.random()
R2 = sf.Rot3.random()

# Composition
display(R1.compose(R2))  # For rotations this is the same as R1 * R2
display(R1 * R2)


# Identity
R_identity = sf.Rot3.identity()
display(R1)
display(R_identity * R1)


# Inverse
R1_inv = R1.inverse()
display(R_identity)
display(R1_inv * R1)


# Between
R_delta = R1.between(R2) #求R1到R2的增量
display(R1 * R_delta)
display(R2)



"""
Lie Group operations
Rotations, poses, and matrices all implement the “LieGroup” interface, meaning that they each have a tangent space. There are many great references on Lie groups out there already, so instead of introducing them here, we recommend checking out Frank Dellaert’s, Ethan Eade’s, or JL Blanco’s tutorials. In SymForce, objects which are a Lie Group can:

Be used to compute the tangent space vector about the identity element (.to_tangent())

Be constructed from a tangent space vector about the identity element (.from_tangent())

Be perturbed by a tangent space vector about the given element (.retract())

Be used to compute the tangent space perturbation needed to obtain another given element (.local_coordinates())

Be used to compute a jacobian describing the relation between the underlying data of the object (e.g. a quaternion for a rotation) and the tangent space vector about the given element (.storage_D_tangent())
"""

'''
用于计算有关单位元素的切线空间向量 (.to_tangent())
由一个关于单位元素的切线空间向量构造 (.from_tangent())
被给定元素的切空间向量扰动 (.retract())
用于计算获得另一个给定元素所需的切线空间扰动 (.local_coordinates())
用于计算一个雅可比矩阵，描述对象的底层数据(例如一个旋转四元数)与给定元素的切线空间向量之间的关系 (.storage_D_tangent())
'''

# To/From tangent space vector about identity element
R1 = sf.Rot3.random()
tangent_vec = R1.to_tangent()
R1_recovered = sf.Rot3.from_tangent(tangent_vec)

assert len(tangent_vec) == R1.tangent_dim()
display(R1)
display(R1_recovered)


# Tangent space perturbations

# Perturb R1 by the given vector in the tangent space around R1
R2 = R1.retract([0.1, 2.3, -0.5])

# Compute the tangent vector pointing from R1 to R2, in the tangent space
# around R1
recovered_tangent_vec = R1.local_coordinates(R2)

display(recovered_tangent_vec)


# Jacobian of storage w.r.t tangent space perturbation

# We chain storage_D_tangent together with jacobians of larger symbolic
# expressions taken with respect to the symbolic elements of the object (e.g. a
# quaternion for rotations) to compute the jacobian wrt the tanget space about
# the element.
# I.e. residual_D_tangent = residual_D_storage * storage_D_tangent

jacobian = R1.storage_D_tangent()
assert jacobian.shape == (R1.storage_dim(), R1.tangent_dim())
display(jacobian.shape)
print(jacobian)
display(jacobian)


