from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Session, Action
import analytics.base_analysis as tools
from functools import reduce
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.aggregates import StringAgg
from .serializers import SessionSerializer, ExperimentSerializer
import json
from .utils import json_field_arrayAgg

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

    Sends everything that isn't a session operation to the group.
    Not sure if this really needs to be changed.
    """

    def connect(self):
        """
        Called on initial socket connection. Accepts if user is authenticated,
        else, close.
        """
        self.user = self.scope["user"]
        self.session = None

        if self.user.is_anonymous:
            self.close()

        else:
            self.accept()

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Arguments:  decoded json array.
        [
            "message_type",
            dict(other_data)
        ]
        """
        action = content[0]
        if action == "session.connect":
            self.session_connect(**content[1])

        elif action == "session.close":
            self.session_close()

        elif action == "session.delete":
            self.session_delete(**content[1])

        elif action == "session.list":
            self.session_list(**content[1])

        else:
            if not self.session:
                self.send_json([action, {"error": "No session selected."}])
                return
            async_to_sync(self.channel_layer.group_send)(
                str(self.session.id),
                {
                    "type": action,
                    **content[1]
                }
            )

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
        async_to_sync(self.channel_layer.group_discard)(
            str(self.session.id),
            self.channel_name
        )

        # send status
        self.send_json(["session.close", {"status": "success"}])

    def session_delete(self, **kwargs):
        """
        Called by receive_json when session.delete command is received.
        Deletes a session specified by id. Assumes that the session is
        not currently connected.

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

    def data_tags(self, event):
        """
        returns a list of all tags used in company.
        """
        data = self.user.company.tag_set.all().values_list('name', flat=True)
        self.send_json([event["type"], list(data)])

    def data_fieldNames(self, event):
        """
        Returns a set of fields in selected experimetns.
        """
        fields_list = self.base_qs.values_list('experimentData', flat=True)
        fields = reduce(lambda a, b: {**a, **b}, fields_list, {}).keys()

        self.send_json([event["type"], list(fields)])

    def data_fieldData(self, event):
        """
        returns data from requested field(s) from a list of
        experiments.
        """
        experiments = event.get("experiments")
        fields = event.get("fields")

        fields_dict = {}
        for field in fields:
            fields_dict.update(json_field_arrayAgg(field))

        qs = self.user.company.experimentdata_set \
            .filter(experiment_id__in=experiments) \
            .values('experiment') \
            .annotate(**fields_dict)

        self.send_json([event["type"], list(qs)])

    def data_experiments(self, event):
        """
        Used for selecting experiments for analysis tool.
        Returns a list of experiments.

        Takes filter, order_by and search as parameters.
        filter is a dictionary with fields to filter by.
        """
        qs = self.user.company.experiment_set.all()

        q = event.get("search", '')  # search query
        filters = event.get("filters", {})
        order_by = event.get("order_by", None)

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

        self.send_json([event["type"], json.dumps(ExperimentSerializer(qs, many=True).data)])

    def group_echo(self, event):
        self.send_json([event["type"], event["message"]])
