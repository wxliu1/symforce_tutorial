
import symforce
symforce.set_epsilon_to_symbol()

from symforce import codegen
from symforce.codegen import codegen_util

import symforce.symbolic as sf
from symforce.notebook_util import display

output_dir="/root/dev/python_ws/test_sym"

m2 = sf.Matrix(2, 3, [1, 2, 3, 4, 5, 6])

display(sf.Quaternion.symbolic("q"))

def generate_matrix() -> sf.Matrix:
    return sf.Matrix.zeros(15, 1)

residual = generate_matrix()
display(residual)

def testMatrix1(mat: sf.Matrix(15, 15)) -> sf.Matrix:
    #
    return mat

m15 = sf.Matrix.zeros(15, 15)
display(testMatrix1(m15))

testMatrix1_codegen = codegen.Codegen.function(
    func=testMatrix1,
    config=codegen.CppConfig(),
)
testMatrix1_data = testMatrix1_codegen.generate_function(output_dir)

def testMatrix2(P_old: sf.M33) -> sf.Matrix33:
    # P_new = sf.Matrix33(1, 2, 3, 4, 5, 6, 7, 8, 9) #sf.Matrix(3, 3,)
    # display(P_new)
    P_new = sf.M33()
    for index in range(3):
        for j in range(3):
            if index > j:
                P_new[index,j] = 0
            else:
                P_new[index,j] = P_old[index,j]

    # display(P_new)

    return P_new

P_old = sf.Matrix33(1, 2, 3, 4, 5, 6, 7, 8, 9)
display(testMatrix2(P_old))

mat2_codegen = codegen.Codegen.function(
    func=testMatrix2,
    config=codegen.CppConfig(),
)
# mat2_data = mat2_codegen.generate_function(output_dir)