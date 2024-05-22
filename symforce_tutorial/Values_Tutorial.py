"""
Values objects are ordered dict-like containers used to store multiple heterogeneous objects, normally for the purpose of function generation.

Typically a Values object will first be created to defines a number of different symbolic inputs (e.g. rotations, translations, scalars, poses, cameras, etc.). Then, a second Values object will be created to describe the objects to be returned from the function, which will be composed of the symbolic elements defined by the input Values object.
"""
# 值对象是类似于字典的有序容器，用于存储多个异构对象，通常用于生成函数

# Setup
import symforce

symforce.set_symbolic_api("sympy")
symforce.set_log_level("warning")

import symforce.symbolic as sf
from symforce.notebook_util import display
from symforce.values import Values


inputs = Values(
    x=sf.Symbol("x"),
    y=sf.Rot2.symbolic("c"),
)
display(inputs)


# The .add() method can add a symbol using its name as the key:
inputs.add(sf.Symbol("foo"))
display(inputs)


# Adding sub-values are well encouraged:
x, y = sf.symbols("x y")
expr = x**2 + sf.sin(y) / x**2
inputs["states"] = Values(p=expr)
display(inputs)


# A Values serializes to a depth-first traversed list. This means it implements StorageOps:
display(inputs.to_storage())


# We can also get a flattened lists of keys and values, with . separation for sub-values:
display(inputs.items_recursive())


# Note that there is a .keys_recursive() and a .values_recursive() which return flattened lists of keys and values respectively:
display(inputs.keys_recursive())
display(inputs.values_recursive())


"""
To fully reconstruct the types in the Values from the serialized scalars, we need an index that describes which parts of the serialized list correspond to which types. The spec is T.Dict[str, IndexEntry] where IndexEntry has attributes offset, storage_dim, datatype, shape, item_index:
"""
index = inputs.index()
display(index)


# With a serialized list and an index, we can get the values back:
inputs2 = Values.from_storage_index(inputs.to_storage(), index)
assert inputs == inputs2
display(inputs2)


# The item_index is a recursive structure that can contain the index for a sub-values:
# item_index是一个递归结构，则包含子值index
item_index = inputs.index()["states"].item_index
assert item_index == inputs["states"].index()
display(item_index)


# 显示单个index
display(inputs.index()["foo"])
display(inputs.index()["y"])


# We can also set sub-values directly with dot notation in the keys. They get split up:
inputs["states.blah"] = 3
display(inputs)


# The .attr field also allows attribute access rather than key access:
assert inputs["states.p"] is inputs["states"]["p"] is inputs.attr.states.p
display(inputs.attr.states.p)


"""
Finally, SymForce adds the concept of a name scope to namespace symbols. Within a scope block, symbol names get prefixed with the scope name:
"""
with sf.scope("params"):
    s = sf.Symbol("cost")
display(s) # 输出params.cost

display(sf.Symbol("cost2"))


"""
A common use case is to call a function that adds symbols within your own name scope to avoid name collisions. You can also chain name scopes:
scope名字作为Values的key
"""
v = Values()
v.add(sf.Symbol("x"))
with sf.scope("foo"):
    v.add(sf.Symbol("x"))
    with sf.scope("bar"):
        v.add(sf.Symbol("x"))
display(v)
display(v.attr.foo.bar.x)


"""
The values class also provides a .scope() method that not only applies the scope to symbol names but also to keys added to the Values:
Values类也提供了scope()方法，不仅应用scope到符号名称上面，而且也作为Values的Keys
值类还提供了一个.scope()方法，它不仅将作用域应用于符号名称，还应用于添加到值中的键
"""
v = Values()
with v.scope("hello"):
    v["y"] = x**2
    v["z"] = sf.Symbol("z")
display(v)

"""
This flexible set of features provided by the Values class allows conveniently building up large expressions, and acts as the interface to code generation.
值类提供的这一组灵活的特性允许方便地构建大型表达式，并充当代码生成的接口。
"""





"""
Lie Group Operations
One useful feature of Values objects is that element-wise Lie group operations on can be performed on them.
值对象的一个有用特性是，可以对它们执行元素级的李群操作。
"""

lie_vals = Values()
lie_vals["scalar"] = sf.Symbol("x")
lie_vals["rot3"] = sf.Rot3.symbolic("rot")

sub_lie_vals = Values()
sub_lie_vals["pose3"] = sf.Pose3.symbolic("pose")
sub_lie_vals["vec"] = sf.V3.symbolic("vec")

lie_vals["sub_vals"] = sub_lie_vals

display(lie_vals)
"""
全部手敲的输出:
Values(
  scalar: x,
  rot3: <Rot3  <Q xyzw=[rot_x, rot_y, rot_z, rot_w]>>,
  sub_vals: Values(
    pose3: <Pos3  R=<Rot3 <Q xyzw=[pose.R_x, pose.R_y, pose.R_z, pose.R_w]>>, t=(pose.t0, pose.t1, pose.t2)>,
    vec: Matrix([
[vec0],
[vec1],
[vec2]]),
    ),
)
"""
# 从教程拷贝的输出
"""
Values(
  scalar: x,
  rot3: <Rot3 <Q xyzw=[rot_x, rot_y, rot_z, rot_w]>>,
  sub_vals:   Values(
    pose3: <Pose3 R=<Rot3 <Q xyzw=[pose.R_x, pose.R_y, pose.R_z, pose.R_w]>>, t=(pose.t0, pose.t1, pose.t2)>,
    vec: Matrix([
[vec0],
[vec1],
[vec2]]),
  ),
)
"""


display(lie_vals.tangent_dim())
display(lie_vals.to_tangent())
display(len(lie_vals.to_tangent()))


"""
Importantly, we can compute the jacobian of the storage space of the object with respect to its tangent space:
"""
display(lie_vals.storage_D_tangent())

"""
输出维数(15*13), List有15维，切线空间有13维:
Matrix([
[1,        0,        0,        0,           0,           0,           0, 0, 0, 0, 0, 0, 0],
[0,  rot_w/2, -rot_z/2,  rot_y/2,           0,           0,           0, 0, 0, 0, 0, 0, 0],
[0,  rot_z/2,  rot_w/2, -rot_x/2,           0,           0,           0, 0, 0, 0, 0, 0, 0],
[0, -rot_y/2,  rot_x/2,  rot_w/2,           0,           0,           0, 0, 0, 0, 0, 0, 0],
[0, -rot_x/2, -rot_y/2, -rot_z/2,           0,           0,           0, 0, 0, 0, 0, 0, 0],
[0,        0,        0,        0,  pose.R_w/2, -pose.R_z/2,  pose.R_y/2, 0, 0, 0, 0, 0, 0],
[0,        0,        0,        0,  pose.R_z/2,  pose.R_w/2, -pose.R_x/2, 0, 0, 0, 0, 0, 0],
[0,        0,        0,        0, -pose.R_y/2,  pose.R_x/2,  pose.R_w/2, 0, 0, 0, 0, 0, 0],
[0,        0,        0,        0, -pose.R_x/2, -pose.R_y/2, -pose.R_z/2, 0, 0, 0, 0, 0, 0],
[0,        0,        0,        0,           0,           0,           0, 1, 0, 0, 0, 0, 0],
[0,        0,        0,        0,           0,           0,           0, 0, 1, 0, 0, 0, 0],
[0,        0,        0,        0,           0,           0,           0, 0, 0, 1, 0, 0, 0],
[0,        0,        0,        0,           0,           0,           0, 0, 0, 0, 1, 0, 0],
[0,        0,        0,        0,           0,           0,           0, 0, 0, 0, 0, 1, 0],
[0,        0,        0,        0,           0,           0,           0, 0, 0, 0, 0, 0, 1]])
"""




"""
This means that we can use the elements of the object to compute a residual, and then compute the jacobian of such a residual with respect to the tangent space of our values object.
意味着可以用Values对象的元素计算一个残差，然后计算残差关于Values对象的切线空间的jacobian
"""

residual = sf.Matrix(6, 1)
# 下面这行的意义：旋转R乘以向量p, 即: Rp
residual[0:3, 0] = lie_vals["rot3"] * lie_vals["sub_vals.vec"]
# 下面这行的意义：位姿T乘以坐标p, 即: Tp = Rp + t
residual[3:6, 0] = lie_vals["sub_vals.pose3"] * lie_vals["sub_vals.vec"]
display(residual)

# 下面这行的意义：残差对切线空间的状态量求导
residual_D_tangent = residual.jacobian(lie_vals)
display(residual_D_tangent.shape)
display(residual_D_tangent)

