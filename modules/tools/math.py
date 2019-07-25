import math as pymath
from math import *


"""
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign',
'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial',
'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite',
'isinf', 'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi',
'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc']
"""


def expression(operands, operators):
    return pretty(f"{' '.join([f'{operands[i]} {operators[i]}' for i in range(len(operators))])} {operands[-1]}")


def pretty(exp):

    operators = {
        '*': '×',
        '/': '÷'
    }

    for item, pretty in operators.items():
        exp = exp.replace(item, pretty)

    return exp


def number(begin, end, step):

    numbers = []
    begin, end = (begin, end) if begin <= end else (end, begin)

    while begin <= end:
        numbers.append(int(begin) if int(begin) == begin else begin)
        begin += step

    return numbers

def calc(exp):

    operators = {
        '×': '*',
        '÷': '/'
    }

    for item, pretty in operators.items():
        exp = exp.replace(item, pretty)

    result = eval(exp)
    return int(result) if int(result) == result else result


def guess(num, level):
    pass