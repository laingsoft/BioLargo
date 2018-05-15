from django.db.models import Func, Avg, Sum


class Log(Func):
    function = 'log'
    arity = 1


class Ln(Func):
    function = 'ln'
    arity = 1


class Sqrt(Func):
    function = 'sqrt'
    arity = 1


class Abs(Func):
    function = 'abs'
    arity = 1


class Add(Func):
    function = ''
    arg_joiner = '+'


class Subtract(Func):
    function = ''
    arg_joiner = '-'


class Divide(Func):
    function = ''
    arg_joiner = '/'


class Multiply(Func):
    function = ''
    arg_joiner = '*'


class Exponent(Func):
    function = ''
    arg_joiner = '^'


# A dictionary of operations with the number of expressions needed, and order.
# 0: exponents
# 1: multiplication and division
# 2: addition and subtraction
# 3: Anything delimited by brackets.
OPERATIONS = {
    "log": (Log, 1, 3),
    "ln": (Ln, 1, 3),
    "avg": (Avg, 1, 3),
    "sum": (Sum, 1, 3),
    "sqrt": (Sqrt, 1, 3),
    "abs": (Abs, 1, 3),
    "+": (Add, 2, 2),
    "-": (Subtract, 2, 2),
    "*": (Multiply, 2, 1),
    "^": (Exponent, 2, 0),
    "/": (Divide, 2, 1)
}
