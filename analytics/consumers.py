from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Session, Action
import analytics.base_analysis as tools
from functools import reduce
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.aggregates import StringAgg
from .serializers import SessionSerializer, ExperimentSerializer
import json

TOOLS = {
    'max': tools.MaxTool,
    'min': tools.MinTool,
    'avg': tools.AvgTool,
    'stdv': tools.STDVTool,
    'variance': tools.VarianceTool,
    'mode': tools.ModeTool,
    'median': tools.MedianTool,
    'equation': tools.EquationTool
}


class AnalyticsConsumer(JsonWebsocketConsumer):
    """
    This consumer handles websocket connections for analysis.
    """

    def connect(self):
        """
        Called on initial socket connection. Accepts if user is authenticated,
        else, close.
        """
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            self.close()

        else:
            self.accept()

    def session_list(self, **kwargs):
        """
        Called by receive_json when session.list command is received.
        gets a list of all sessions from the user.

        Arguments:
            search: a search query for session name or project name
        """

        search_query = kwargs.get("search", '')
        qs = self.user.session_set.all()

        vector = SearchVector(
            'name',
            'project__name'
        )

        if search_query:
            qs = qs.annotate(search=vector).filter(search=search_query)

        sessions = SessionSerializer(qs, many=True).data

        self.send_json(['session.list', sessions])

    def session_connect(self, **kwargs):
        """
        Called by receive_json when session.connect command is received.
        connects user to a specified session, if an id is provided, else,
        a new session is created if name and project are given.
        """
        pk = kwargs.get("pk", None)

        if pk:
            # get session object
            try:
                self.session = self.user.session_set.get(pk=pk)
            except Session.DoesNotExist:
                self.send_json(["session.connect", {"status": "error"}])
                return
        else:
            name = kwargs.get("name")
            project = kwargs.get("project_id")

            self.session = Session.objects.create(
                name=name,
                project_id=project,
                user=self.user
            )

        # connect
        async_to_sync(self.channel_layer.group_add)(str(self.session.id), self.channel_name)
        self.send_json(["session.connect", {"status": "success"}])

    def session_close(self, **kwargs):
        """
        Called by receive_json when session.close command is received.
        closes the current sessions.

        Arguments: none.
        """
        self.session = None

        # leave group

        # send status
        self.send_json({**kwargs, 'status': 'success'})

    def session_delete(self, **kwargs):
        """
        Called by receive_json when session.delete command is received.
        Deletes a session specified by id.

        Arguments:
            pk: id of session.
        """
        pk = kwargs.get("pk")

        try:
            session = self.user.session_set.get(pk=pk)
        except Session.DoesNotExist:
            self.send_json(['session.delete', {'status': 'error'}])

        session.delete()

        self.send_json(['session.delete', {'status': 'success'}])

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Arguments:  decoded json array.
        [
            "message_type",
            {
                data
            }
        ]
        """
        print(content)

        action = content[0]
        if action == "session.connect":
            self.session_connect(**content[1])

        elif action == "group.echo":
            async_to_sync(self.channel_layer.group_send)(
                str(self.session.id),
                {
                    "type": "group.echo",
                    "message": content[1]["message"]
                }
            )

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
        qs = self.user.company.experiment_set.all()

        q = kwargs.get("search", '')  # search query
        filters = kwargs.get("filters", {})
        order_by = kwargs.get("order_by", None)

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

        self.send_json({'data': json.dumps(ExperimentSerializer(qs, many=True).data)})

    def group_echo(self, event):
        print(event)
        self.send_json(event["message"])
