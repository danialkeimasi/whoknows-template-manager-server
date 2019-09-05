import itertools
import math as pymath
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


def randint(begin, end, func=None):
    return choose(number(begin, end, func=func), 0)


def number(begin, end, step=1, func=None):
    numbers = []
    begin, end = (begin, end) if begin <= end else (end, begin)
    step = int(step)

    while begin <= end:
        if func is None or func(begin):
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

    return operand_range_sorted[:2] + choose(operand_range, 1)


def choice_generator(operands, operators, level):
    answer = calc(expression(operands, operators))

    operands_guess_list = [guess_operand(operand, level) for operand in operands]
    operands_choice = list(itertools.product(*operands_guess_list))
    expressions_choice = [expression(operand, operators) for operand in operands_choice]

    choices = list(set([calc(exp) for exp in expressions_choice]) - set([answer, 0]))
    choices = sorted(choices, key=lambda x: fabs(answer - x))

    part = 10 - level
    r = len(choices) // 11 * part
    choices = choices[r:  r + 10]

    return choices


def divisors(n):
    if n < 1:
        return []

    divs = [1, n]
    for i in range(2, int(pymath.sqrt(n)) + 1):
        if n % i == 0:
            divs += [i, n // i]

    return sorted(list(set(divs)))


def is_prime(n):
    return n > 1 and (n == 2 or len(divisors(n)) == 2)


def is_composite(n):
    return n > 1 and not is_prime(n)
