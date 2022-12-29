import numpy as np
import sympy as sp

def derive(function):
    x = sp.Symbol('x')
    f = sp.sympify(function)
    return f.diff(x)
def integrate(function):
    x = sp.Symbol('x')
    f = sp.sympify(function)
    return sp.integrate(f, x)

x = sp.Symbol('x')
func = x**2

derivative = derive(func)
integral = integrate(func)

print(f"The derivative is {derivative.latex()}")
print(f"The integral is {integral.latex()}")