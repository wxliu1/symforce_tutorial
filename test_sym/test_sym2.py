


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

def max(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    if a > b:
        retval = a #f"a > b"
    else:
        retval = b #f"a < b"
    return retval
 
print(max(5,4))

def sum(a: sf.Scalar, b: sf.Scalar) -> sf.Scalar:
    retval = None
    retval = a + b
    return retval

print(sum(3, 4))



def matrix_multiply(a: sf.M55, b: sf.M55) -> sf.M55:
    retval = None
    retval = a * b
    return retval

m1 = sf.M55.symbolic("a")
display(m1)


matrix_multiply_codegen = codegen.Codegen.function(
    func=matrix_multiply,
    config=codegen.CppConfig(),
)
    
output_dir="/root/dev/python_ws/test_sym"
matrix_multiply_data = matrix_multiply_codegen.generate_function(output_dir)


max_codegen = codegen.Codegen.function(
    func=max,
    config=codegen.CppConfig(),
)
    
output_dir="/root/dev/python_ws/test_sym"
max_data = max_codegen.generate_function(output_dir)


sum_codegen = codegen.Codegen.function(
    func=sum,
    config=codegen.CppConfig(),
)
    
output_dir="/root/dev/python_ws/test_sym"
sum_data = sum_codegen.generate_function(output_dir)  
