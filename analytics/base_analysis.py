from django.db.models import Max, Min, Sum, Avg, StdDev, Variance
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import FloatField
from django.db.models.functions import Cast
from .aggregates import Mode, Percentile
# from statistics import median, mode, stdev, variance
import re
from django.utils.text import slugify
from functools import reduce
from django.db.models import Func, F


# Some math functions from postgres.
class Log(Func):
    function = 'log'


class Ln(Func):
    function = 'ln'


class Sqrt(Func):
    function = 'sqrt'


class Abs(Func):
    function = 'abs'


class Tool:
    """
    Base tool for all analysis. Contains information to query database.
    parameters:
        - base_qs: Base queryset of ExperimentData (stored by the session)
        - filters: a dictionary of additional filters for qs.
        - fields: a list of field names (string) for operation.
    """
    def __init__(self, base_qs, field, *args, **kwargs):
        self.base_qs = base_qs
        self.field = field

    def evaluate(self):
        pass


class EquationTool(Tool):
    """
    Calculates equations.
    Takes same arguements as Tool, without the fields argument, and
    with an additional equations list.
    """
    BINARY_OPS = {'+', '-', '*', '/', '^'}
    UNARY_OPS = {
        'LOG': Log,
        'LN': Ln,
        'SQRT': Sqrt,
        'ABS': Abs
    }

    def __init__(self, base_qs, *args, **kwargs):
        super().__init__(base_qs, None, **kwargs)
        self.equations = kwargs.get('equations')  # a list of strings
        self.vars = dict()  # a dictionary of annotations needed. key=slugify('field')
        self.annotations()

    def tokenize_equation(self, equation):
        """
        Breaks equation up into a list of individual tokens.

        Ex.
        "AVG(LOG('StockCFU [CFU/mL]') - LOG('RemainingCFU [CFU/mL]'))"

        will return
        ['AVG', '(', 'LOG', '(', "'StockCFU [CFU/mL]'", ')', '-',
        'LOG', '(', "'RemainingCFU [CFU/mL]'", ')', ')']
        """
        pattern = "('[^']+'|[\\+\\-*\\/]|\w+|[\\(\\)])"
        pattern = re.compile(pattern)
        return pattern.findall(equation)

    def get_field(self, field_name):
        """
        gets json fields. field_name is the json key.
        """
        return Cast(
                KeyTextTransform(
                    field_name,
                    'experimentData'),
                FloatField())

    def combine_annotations(self, annotations):
        """
        Combines a list of dictionaries of annotations into one dictionary.
        """
        return reduce(lambda a, b: {**a, **b}, annotations, {})

    def build_annotation(self, tokens):
        """
        Builds the annotation part of the equation to be evaluated.
        """
        op_stack = []
        var_stack = []
        open_bracket = 0  # for syntax checking.

        for token in tokens:
            if token == '(':
                open_bracket += 1

            elif token == ')':
                # check if there is an open bracket
                if not open_bracket:
                    # Syntax error if there is no open bracket at all.
                    raise ValueError
                open_bracket -= 1

                op = op_stack.pop()
                while op != '(':
                    if op in self.UNARY_OPS:
                        pass
                    if op in self.BINARY_OPS:
                        pass


                # pop from var stack
                # perform operation
                # append back to var stack.

            elif token[0] == '\'':
                # check if a variable
                var = self.vars(slugify(token[1:-1]), self.get_field(token[1:-1]))
                if slugify(token[1:-1]) not in self.vars:
                    self.vars[slugify(token[1:-1])] = var

                var_stack.append(var)

            elif token in self.UNARY_OPS or token in self.BINARY_OPS:
                op_stack.append(token)

            else:
                # if it doesn't fit anything then it's a syntax error.
                raise ValueError

    def evaluate(self):
        for equation in self.equations:
            tokens = self.tokenize_equation(equation)
            self.build_annotation(tokens)


class BaseAggregateTool(Tool):
    """
    Base tool for aggregrate functions performed on database.
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
