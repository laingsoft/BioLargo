from django.db.models import Func, Avg, Sum
from operator import add, pow, sub, truediv, mul

# Unrelated to math, but used for the return value:
class to_json(Func):
    function = 'to_json'
    template = '%(function)s((%(expressions)s))'

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
    "+": (add, 2, 2),
    "-": (sub, 2, 2),
    "*": (mul, 2, 1),
    "^": (pow, 2, 0),
    "/": (truediv, 2, 1)
}
