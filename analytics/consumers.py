from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Session, Action
import analytics.base_analysis as tools
from functools import reduce
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.aggregates import StringAgg
from api.serializers import simpleExperimentSerializer
import json

TOOLS = {
    'max': tools.MaxTool,
    'min': tools.MinTool,
    'avg': tools.AvgTool,
    'stdv': tools.STDVTool,
    'variance': tools.VarianceTool,
    'mode': tools.ModeTool,
    'median': tools.MedianTool
}


class AnalyticsConsumer(JsonWebsocketConsumer):
    """
    This consumer handles websocket connections for analysis.
    """

    def connect(self):
        """
        called on initial connection
        """

        self.user = self.scope["user"]

        if self.user.is_anonymous:
            self.close()

        else:
            self.base_qs = self.user.company.experimentdata_set.all()
            self.base_exeriment_set = self.user.company.experiment_set.all()
            self.accept()

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Arguments:  content - decoded JSON (a dictionary)
        """
        action = content.get('action')

        if action == 'get_tags':
            self.get_tags()

        if action == 'get_fields':
            self.get_fields()

        if action == 'get_experiment_list':
            filters = content.get('filters')
            order_by = content.get('order_by')
            self.get_experiment_list(filters=filters, order_by=order_by)

        if action == 'get_data':
            params = content.get('params')
            self.get_data(params)

    def disconnect(self, code):
        """
        Called when websocket connetion is closed.
        """
        pass

    def get_tags(self):
        """
        returns a list of tags of data set.
        """
        data = self.user.company.tag_set.all().values_list('name', flat=True)
        self.send_json({'data': list(data)})

    def get_fields(self):
        fields_list = self.base_qs.values_list('experimentData', flat=True)
        fields = reduce(lambda a, b: {**a, **b}, fields_list, {}).keys()

        self.send_json({'fields': list(fields)})

    def create_action(self, experiments):
        """
        Creates new action object for
        """
        pass

    def get_data(self, exp_set, params):
        """
        returns requested data. Will apply and transformations and aggregation.
        Handled by the database. Used when getting data for graphs.

        exp_set: a list of ids of experiments to get data from
        params: a dictionary.

        params dictionary format:
        {
            filters: {}
            expressions: [""] // list of expressions or fields
                ex. 'RemainingCFU [CFU/mL]' or
                LOG('StockCFU [CFU/mL]') - LOG('RemainingCFU [CFU/mL]')"
                Single quotes around field names required.
            group_by: [] // A list of fields to group by.
            replicates: boolean value. effect grouping.
        }

        Ex.
        {
            filters: {id: [1,2,3]},
            expression: "AVG(LOG('StockCFU [CFU/mL]') - LOG('RemainingCFU [CFU/mL]'))"
            group_by: ["Time [min]"]
        }

        Result: average log removal of experiments 1, 2 and 3 over time
        """

        # get action object with id.
        # base experimentdata for this action
        # qs = self.base_qs.filter(experiment__id__in=exp_set)

        # if there is a group_by, aggregate.
        # else, annotate and or return requested field values.

        self.send_json({'data': 'get data test'})

    def get_experiment_list(self, **kwargs):
        """
        Used for selecting experiments for analysis tool.
        Returns a list of experiments.

        Takes filter, order_by and search as parameters.
        filter is a dictionary with fields to filter by.
        """
        qs = self.base_exeriment_set

        q = kwargs.get("search", '').strip()  # search query
        filters = kwargs.get("filters", {})
        order_by = kwargs.get("order_by", None)  # string. -field for descending

        # Search vector used
        vector = SearchVector(
            'friendly_name',
            'project__name',
            StringAgg('tags__name', delimiter=' '),
            'sop__name'
        )
        if q:
            qs = qs.annotate(search=vector).filter(search=q)

        if filters:
            qs = qs.filter(**filters)

        if order_by:
            qs = qs.order_by(order_by)

        self.send_json({'data': json.dumps(simpleExperimentSerializer(qs, many=True).data)})
