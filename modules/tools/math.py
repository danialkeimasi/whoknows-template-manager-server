import math as pymath
from math import *


"""
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign',
'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial',
'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite',
'isinf', 'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi',
'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc']
"""


def poly(operands, operators, show=False):
    if show:
        for i, operator in enumerate(operators):
            if operator == '*':
                operators[i] = '×'
            elif operator == '/':
                operators[i] = '÷'

    return f"{' '.join([f'{operands[i]} {operators[i]}' for i in range(len(operators))])} {operands[-1]}"
