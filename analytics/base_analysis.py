from django.db.models import Max, Min, Sum, Avg, StdDev, Variance
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import FloatField
from django.db.models.functions import Cast
from .aggregates import Mode, Percentile
from django.db import connection
# from statistics import median, mode, stdev, variance


class Tool:
    """
    Base tool for all analysis. Contains information to query database.
    parameters:
        - base_qs: Base queryset (stored by the session)
        - filters: a dictionary of additional filters for qs.
        - fields: a list of field names (string) for operation.
    """
    def __init__(self, base_qs, field, filters=[], *args, **kwargs):
        self.base_qs = base_qs
        self.filters = filters
        self.field = field

    def evaluate(self):
        pass


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
        query = self.base_qs.filter(*self.filters) \
            .annotate(
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
    Can't get query to work with ORM, so this one is done by executing raw SQL.
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
