import math as pymath
import itertools

from decimal import Decimal
from math import *

from modules.tools.functions import choose


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
    step = int(step)

    while begin <= end:
        numbers.append(int(begin) if int(begin) == begin else begin)
        begin = float(Decimal(str(begin)) + Decimal(str(step)))

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


def guess_operand(num, level):
    
    r = max(5, int(num // pymath.log(pymath.fabs(num) + 2, 2)))
    operand_range = number(float(Decimal(str(num)) - Decimal(str(r))), float(Decimal(str(num)) + Decimal(str(r))), 1)
    operand_range = list(set(operand_range))
    
    mod = 2 if level >= 7 else None

    if mod:
        operand_range = [item for item in operand_range if item % mod == num % mod]
    
    operand_range_sorted = sorted(operand_range, key=lambda x: fabs(num - x))

    return operand_range[:2] + choose(operand_range, 1)

                  
def choice_generator(operands, operators, level):
    answer = calc(expression(operands, operators))

    operands_guess_list = [guess_operand(operand, level) for operand in operands]
    operands_choice = list(itertools.product(*operands_guess_list))
    expressions_choice = [expression(operand, operators) for operand in operands_choice]
    
    choices = list(set([calc(exp) for exp in expressions_choice]) - set([answer]))
    choices = sorted(choices, key=lambda x: fabs(answer - x))
    
    part = 10 - level
    r = len(choices) // 11 * part
    choices = choices[ r :  r + 10]

    return choices



