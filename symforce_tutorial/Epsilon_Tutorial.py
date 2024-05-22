"""
This notebook describes the epsilon mechanism by which numerical singularities are handled in SymForce. The paper addresses the theory in Section VI, and this tutorial demonstrates the idea through examples.

The basic concept is that it is common to have functions in robotics that are smooth but have singularities at given points. Handwritten functions tend to handle them by adding an if statement at the singularity with some kind of approximation or alternate formulation. This is harder to do with symbolic expressions, and also is not kind to branch prediction. SymForce addresses this with a different method - shifting the input to the function away from the singular point with an infinitesimal variable 
 (epsilon). This approach is simple and fast for a useful class of removable singularities, with negligible effect to output values for sufficiently small epsilon.

All functions in SymForce that have singularities take epsilon as an argument. In a numerical context, a very small floating point number should be passed in. In the symbolic context, an epsilon symbol should be passed in. Epsilon arguments are currently optional with zero defaults. This is convenient so that playing with expressions in a notebook doesn’t require passing epsilons around. However, this is dangerous and it is extremely important to pass epsilons to get robust behavior or when generating code. Because of this, there are active efforts to make a more intelligent mechanism for the default epsilon to make it less of a footgun to accidentally forget an epsilon and end up with a NaN.

Goal
We have a function f(x).

In the simplest case, we’re trying to fix a removable singularity at x=0, i.e. f(x).subs(x, 0) == sm.S.NaN

Libraries often do this by checking whether the value of x is close to 0, and using a different method for evaluation there, such as a Taylor expansion. In symbolic expressions, branching like this is messy and expensive.

The idea is to instead make a function f(x, eps) so the value is not NaN, when eps is a small positive number:
f(x, eps).subs(x, 0) != sm.S.NaN
We usually also want that the derivative is not NaN:
f(x, eps).diff(x).subs(x, 0) != NaN
For value continuity we want to match the limit:
f(x, eps).subs(x, 0).limit(eps, 0) == f(x).limit(x, 0)
For derivative continuity we want to match the limit: f(x, eps).diff(x).subs(x, 0).limit(eps, 0) == f(x).diff(x).limit(x, 0)
"""


import numpy as np
import plotly.express as px
import sympy as sm

x = sm.Symbol("x")
eps = sm.Symbol("epsilon")


"""
An example: sin(x) / x
For the whole section below, let’s pretend x is positive so x=-epsilon is not a fear. We’ll address that later.
"""

# The function `sin(x) / x` looks like this:
def f(x):
    return sm.sin(x) / x


print(f(x))

# And its graph:
x_numerical = np.linspace(-5, 5)
px.line(x=x_numerical, y=np.vectorize(f, otypes=[float])(x_numerical))


# It has a removable singularity at 0, of the form 0/0, which gives NaN:
print(f(x).subs(x, 0))

# The derivative has the same issue:
f(x).diff(x).subs(x, 0)

"""
One thought to fix this might be to just push the denominator away from 0. This does resolve the NaN, but it produces the wrong value! (Remember, the value at x=0 should be 1)
"""
def f(x, eps):
    return sm.sin(x) / (x + eps)


f(x, eps).subs(x, 0)

# Similarly, the derivative is wrong, and actually diverges (it should be 0):
f(x, eps).diff(x).subs(x, 0)

f(x, eps).diff(x).subs(x, 0).limit(eps, 0)


"""
Instead, what we want to do is perturb the input away from the singularity. Effectively, we’re shifting the graph of the function to the left. For removable singularities in well-behaved functions, the error introduced by this is proportional to epsilon. That looks like this:
"""

def f(x, eps):
    x_safe = x + eps
    return sm.sin(x_safe) / x_safe


f(x, eps).subs(x, 0)

f(x, eps).subs(x, 0).limit(eps, 0)

f(x, eps).diff(x).subs(x, 0)

f(x, eps).diff(x).subs(x, 0).limit(eps, 0)

