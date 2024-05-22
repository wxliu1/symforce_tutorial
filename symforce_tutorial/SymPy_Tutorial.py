
import symforce

symforce.set_symbolic_api("symengine")

import symforce.symbolic as sf
from symforce.notebook_util import display
from symforce.notebook_util import print_expression_tree

x = sf.Symbol("x")
y = sf.Symbol("y")

expr = x**2 + sf.sin(y) / x**2
display(expr)

print_expression_tree(expr)

display(expr.subs({x: 1.2, y: 0.4}))

display(expr.diff(y))

display(sf.series(expr, y))
