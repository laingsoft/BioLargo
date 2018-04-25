from django.db.models import Max, Min, Sum, Avg, StdDev, Variance
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import FloatField
from django.db.models.functions import Cast
from .aggregates import Mode, Percentile
import re
from django.db.models import F
from .operations import OPERATIONS
from .utils import json_field_format
from django.contrib.postgres.aggregates import ArrayAgg


class Tool:
    """
    Base tool for all analysis. Contains information to query database.
    parameters:
    """
    def __init__(self, **kwargs):
        self.base_qs = self.get_base_queryset(
            kwargs.get("company"),
            kwargs.get("experiments"))

    def get_base_queryset(self, company, experiments):
        qs = company.experimentdata_set.filter(
            experiment__in=experiments)
        return qs

    def evaluate(self):
        pass


class EquationTool(Tool):
    """
    Calculates equations.
    Takes same arguements as Tool, without the fields argument, and
    with an additional equations list. Assumes that the equation is
    properly formatted, with brackets around functions, where needed.
    Formatting is not check explicitly.

    Takes a list of equations to calculate along with the arguments for base
    tool
    """
    pattern = re.compile("('[^']+'|[\\+\\-*\\/]|\w+|[\\(\\)])|\d+")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vars = {}
        self.equations = kwargs.get("equations")
        self.parsed = {}  # dictionary to pass into annotate later

    def tokenize_equation(self, equation):
        """
        Breaks equation up into a list of individual tokens using regex.

        Ex.
        "AVG(LOG('StockCFU [CFU/mL]') - LOG('RemainingCFU [CFU/mL]'))"

        will return
        ['AVG', '(', 'LOG', '(', "'StockCFU [CFU/mL]'", ')', '-',
        'LOG', '(', "'RemainingCFU [CFU/mL]'", ')', ')']
        """

        return self.pattern.findall(equation)

    def to_postfix(self, tokens):
        """
        Turns the tokenized infix expression into postfix form.
        (is actually postfix, but it'll be popped from back)
        Returns a list
        """
        postfix = []
        op_stack = []
        for token in tokens:
            if token in OPERATIONS:
                op = OPERATIONS[token]

                if op_stack and op_stack[-1][2] > op[2]:
                    popped = op_stack.pop()
                    while popped != '(' and op_stack:
                        postfix.append(popped)
                        popped = op_stack.pop()

                    if popped == '(':
                        # append back a bracket if popped out.
                        op_stack.append('(')

                else:
                    op_stack.append(op)

            elif token[0] == "'":
                token_clean = token.strip("'")
                self.vars.update(json_field_format(token_clean))
                postfix.append(F(token_clean))

            elif token == '(':
                op_stack.append(token)

            elif token == ')':
                op = op_stack.pop()
                try:
                    while op != ('('):
                        postfix.append(op)
                        op_stack.pop()
                except IndexError:
                    raise ValueError("Imbalanced brackets")
                if op_stack:
                    # if the bracket indicates a function, then pop function.
                    if op_stack[-1][2] == 3:
                        postfix.append(op_stack.pop())

        # pop any remaining items off the op_stack
        while op_stack:
            postfix.append(op_stack.pop())

        return postfix

    def to_django(self, postfix):
        """
        takes a postfix expression and converts to a form usable by Django's ORM.
        Errors not caughted by the conversion should be caught here.
        """
        print(postfix)
        vars = []
        for item in postfix:
            print(item)
            print(vars)
            if isinstance(item, tuple):  # if is an operation
                num_args = item[1]

                # check that there are enough arguments for operation.
                if num_args > len(vars):
                    raise ValueError("Not enough arguments for operation")
                args = vars[-num_args:]
                del vars[-num_args:]
                # Apply operation and append back to var stack
                vars.append(item[0](*args))
            else:
                # if it's not an operations then it's a variable (no brackets)
                vars.append(item)

        if len(vars) > 1:
            raise ValueError("Malformed expression")

        return vars[0]

    def evaluate(self):
        for e in self.equations:
            tokens = self.tokenize_equation(e)
            print(tokens)
            postfix = self.to_postfix(tokens)
            self.parsed[e] = ArrayAgg(self.to_django(postfix))

        result = self.base_qs \
            .annotate(**self.vars) \
            .values('experiment') \
            .annotate(**self.parsed)

        return result


class BaseAggregateTool(Tool):
    """
    Base tool for aggregrate functions performed on database. Aggreates
    single fields.
    Aggregate function used must be defined by child classes.
    function: Aggregate function name from postgres
    extra: list of other arguments that need to be passed into function.
    """
    function = None
    extra = []

    def evaluate(self):
        query = self.base_qs.annotate(
                val=Cast(
                    KeyTextTransform(self.field, 'experimentData'),
                    FloatField())) \
            .aggregate(result=self.function('val', *self.extra))

        return query


# ###############
# # Basic tools #
# ###############

class MaxTool(BaseAggregateTool):
    """
    gets the max of a single field.
    """
    function = Max


class MinTool(BaseAggregateTool):
    """
    get the min of a single field.
    """
    function = Min


class AvgTool(BaseAggregateTool):
    """
    gets average of a single field.
    """
    function = Avg


class SumTool(BaseAggregateTool):
    """
    gets sum of values
    """
    function = Sum


# #########################
# # Stats Library Wrapper #
# #########################

class STDVTool(BaseAggregateTool):
    """
    gets standard deviation
    """
    function = StdDev


class VarianceTool(BaseAggregateTool):
    """
    gets variance.
    """
    function = Variance


class ModeTool(BaseAggregateTool):
    """
    gets mode using PostgreSQL's Mode aggregate.
    """
    function = Mode


class MedianTool(BaseAggregateTool):
    """
    gets median.
    """
    function = Percentile
    extra = [0.5]


# ##################
# # Genomics Tools #
# ##################

# class nX_score_tool(Tool):
#     '''
#     Calculates the N[x] score
#     Accepts x_val, where x_val is the percentage of the entire assembly
#     you want to see
#     '''

#     def __init__(self, data, x_val):
#         self.data = data.sort(reverse=True)
#         self.x_val = x_val / 100

#     def evaluate(self):
#         total_sum = sum(self.data)
#         i = 0
#         running_sum = 0
#         while running_sum < (total_sum * self.x_val) :
#             cursor = self.data[i]
#             running_sum += cursor
#             i+=1
#         return cursor

# class ngX_score_tool(Tool):
#     '''
#     calculates the NG[X] score
#     Accepts the x_val and genome size
#     '''
#     def __init__(self, data, x_val, g_size):
#         self.data = data.sort(reverse = True)
#         self.x_val = x_val / 100
#         self.g_size = g_size

#     def evalutate(self):
#         i = 0
#         running_sum = 0
#         while running_sum < (self.g_size * self.x_val):
#             cursor = self.data[i]
#             running_sum += cursor
#             i+=1
#         return cursor
