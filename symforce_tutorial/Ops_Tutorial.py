
# Setup
import symforce

symforce.set_symbolic_api("sympy")
symforce.set_log_level("warning")

import symforce.symbolic as sf
from symforce.notebook_util import display
from symforce.ops import GroupOps
from symforce.ops import LieGroupOps
from symforce.ops import StorageOps
from symforce.values import Values


"""
StorageOps
StorageOps: Data type that can be serialized to and from a vector of scalar quantities.

Methods: .storage_dim(), .to_storage(), .from_storage(), .symbolic(), .evalf(), .subs(), .simplify()

Storage operations are used extensively for marshalling and for operating on each scalar in a type.
"""

# Number of scalars used to represent a Pose3 (4 quaternion + 3 position)
display(StorageOps.storage_dim(sf.Pose3))


# Because we are using concepts, we can operate on types that aren't subtypes
# of symforce
display(StorageOps.storage_dim(float))


# Element-wise operations on lists of objects
display(StorageOps.storage_dim([sf.Pose3, sf.Pose3]))


# Element-wise operations on Values object with multiple types of elements
values = Values(
    pose=sf.Pose3(),
    scalar=sf.Symbol("x"),
)
display(StorageOps.storage_dim(values))  # 4 quaternion + 3 position + 1 scalar


# Serialize scalar
display(StorageOps.to_storage(5))


# Serialize vector/matrix
display(StorageOps.to_storage(sf.V3(sf.Symbol("x"), 5.2, sf.sqrt(5))))


# Serialize geometric type and reconstruct
T = sf.Pose3.symbolic("T")
T_serialized = StorageOps.to_storage(T)
# 从列表数据恢复到位姿sf.Pose3类型的数据
T_recovered = StorageOps.from_storage(sf.Pose3, T_serialized)
display(T)
display(T_serialized)
display(T_recovered)


"""
GroupOps
GroupOps: Mathematical group that implements closure, associativity, identity and invertibility.

Methods: .identity(), .inverse(), .compose(), .between()

Group operations provide the core methods to compare and combine types.
"""

# Identity of a pose
display(GroupOps.identity(sf.Pose3))


# Identity of a scalar (under addition)
display(GroupOps.identity(float))


# Inverse of a vector
display(GroupOps.inverse(sf.V3(1.2, -3, 2)).T)


# Compose two vectors (under addition)
display(GroupOps.compose(sf.V2(1, 2), sf.V2(3, -5)))


# Compose a rotation and its inverse to get identity
R1 = sf.Rot3.from_angle_axis(
    angle=sf.Symbol("theta1"),
    axis=sf.V3(0, 0, 1),
)
display(StorageOps.simplify(GroupOps.compose(R1, R1.inverse()).simplify()))


# Relative rotation using `.between()`
R2 = sf.Rot3.from_angle_axis(
    angle=sf.Symbol("theta2"),
    axis=sf.V3(0, 0, 1),
)
R_delta = GroupOps.between(R1, R2)
display(R2)
display(StorageOps.simplify(GroupOps.compose(R1, R_delta)))



"""
LieGroupOps
LieGroupOps: Group that is also a differentiable manifold, such that calculus applies.

Methods: .tangent_dim(), .from_tangent(), to_tangent(), .retract(), .local_coordinates(), .storage_D_tangent()

Lie group operations provide the core methods for nonlinear optimization.
Familiarity is not expected for all users, but learning is encouraged!
"""

# Underlying dimension of a 3D rotation's tangent space
display(LieGroupOps.tangent_dim(sf.Rot3))


# Exponential map (tangent space vector wrt identity element) for a 2D rotation
angle = sf.Symbol("theta")
rot2 = LieGroupOps.from_tangent(sf.Rot2, [angle])
display(rot2.to_rotation_matrix())
display(rot2)
display(sf.Rot2())
display(sf.Rot2().to_rotation_matrix())


# Logarithmic map (tangent space wrt identity element -> element) of the rotation
display(LieGroupOps.to_tangent(rot2))
# 以下5行，个人测试
display(StorageOps.storage_dim(LieGroupOps.to_tangent(rot2)))
display(sf.Rot3().to_rotation_matrix())
display(LieGroupOps.to_tangent(sf.Rot3.random()))
R = sf.Rot3.symbolic("R")
display(LieGroupOps.to_tangent(R))


# Exponential map of a vector type is a no-op
display(LieGroupOps.from_tangent(sf.V5(), [1, 2, 3, 4, 5]).T)



# Retract perturbs the given element in the tangent space and returns the
# updated element
rot2_perturbed = LieGroupOps.retract(rot2, [sf.Symbol("delta")])
display(rot2_perturbed.to_rotation_matrix())


# Local coordinates compute the tangent space perturbation between one element
# and another
# local_coordinates用于计算切线空间的扰动
display(StorageOps.simplify(LieGroupOps.local_coordinates(rot2, rot2_perturbed)))

display(LieGroupOps.local_coordinates(rot2, rot2_perturbed))




# storage_D_tangent computes the jacobian of the storage space of an object with
# respect to the tangent space around the element.

# A 2D rotation is represented by a complex number, so storage_D_tangent
# represents how that complex number will change given an infinitesimal
# perturbation in the tangent space
display(rot2)
display(LieGroupOps.storage_D_tangent(rot2))

R = sf.Rot3.symbolic("R")
display(LieGroupOps.storage_D_tangent(R))


"""
Using symbolic geometric types and concepts is already very powerful for development and analysis of robotics, but operating on symbolic objects at runtime is much too slow for most applications. However, symbolic expressions can be beautifully set to fast runtime code.
"""
