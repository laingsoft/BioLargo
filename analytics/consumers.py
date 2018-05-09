from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Session, Action
from analytics.base_analysis import EquationTool
from functools import reduce
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.aggregates import StringAgg
from .serializers import SessionSerializer, ExperimentSerializer, ActionSerializer, ProjectSerializer
import json
from django.db.utils import DataError


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
            self.session_list()

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Expected content format:

        {
            type: 'String',
            payload: {
                key: value
            },
            meta: {}
        }
        """
        type_ = content['type']
        payload = content.get('payload', {})

        print(content)

        if type_ == "SESSION.CONNECT":
            self.session_connect(**payload)

        elif type_ == "SESSION.CLOSE":
            self.session_close()

        elif type_ == "SESSION.DELETE":
            self.session_delete(**payload)

        elif type_ == "SESSION.LIST":
            self.session_list(**payload)

        else:
            if not self.session:
                self.send_json(
                    type_,
                    {"error": "No sessions selected"},
                    error=True
                    )
                return
            async_to_sync(self.channel_layer.group_send)(
                str(self.session.id), {
                    "type": type_.lower(),
                    **payload
                }
            )

    def send_json(self, type, payload=None, error=False, close=False, meta=None):
        """
        Overriding default conusmer.
        """
        content = {"type": "SERVER/" + type.upper()}
        if payload:
            content["payload"] = payload
        if error:
            content["error"] = True
        if meta:
            content["meta"] = meta

        super().send_json(content)

    def session_list(self, **kwargs):
        """
        Called by receive_json when session.list command is received.
        gets a list of all sessions from the user.

        Arguments:
            search: a ssuper().send(
            text_data=json.dumps(content)
        )earch query for session name or project name
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

        self.send_json('SESSION.LIST', {"sessions": sessions})

    def session_connect(self, **kwargs):
        """
        Called by receive_json when session.connect command is received.
        connects user to a specified session, if an id is provided, else,
        a new session is created if name and project are given.
        """
        pk = kwargs.get("id", 0)

        assert isinstance(pk, int)

        if pk:
            # get session object
            try:
                self.session = self.user.session_set.get(pk=pk)
            except Session.DoesNotExist:
                self.send_json(
                    "session.connect",
                    {"error: Session does not exist"},
                    error=True)
                return
        else:
            name = kwargs.get("name")
            project = kwargs.get("project")

            try:
                self.session = Session.objects.create(
                    name=name,
                    project_id=project,
                    user=self.user
                )
            except DataError as e:
                self.send_json("SESSION.CONNECT", {'error': "Error creating session"}, error=True)
                return

        # connect
        async_to_sync(self.channel_layer.group_add)(
            str(self.session.id), self.channel_name)
        self.send_json("SESSION.CONNECT", SessionSerializer(self.session).data)

    def session_close(self, **kwargs):
        """
        Called by receive_json when session.close command is received.
        closes the current sessions.

        Arguments: none.
        """
        if self.session:
            # leave group
            async_to_sync(self.channel_layer.group_discard)(
                str(self.session.id),
                self.channel_name
            )
            self.session = None

        # send status
        self.send_json("SESSION.CLOSE")

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
            self.send_json(
                'SESSION.DELETE',
                {"error": "Session does not exist"},
                error=True)

        session.delete()

        self.send_json('SESSION.DELETE')


    def fetch_data(self, event):
        """
        returns data from requested field(s) from a list of
        experiments.

        Arguments:
        - Experiments: a list of ids of experiments to get data from
        - expressions: a list of expressions. can be a single variables or equations
        """
        experiments = event.get("experiments")
        expressions = event.get("expressions")

        if not (experiments and expressions):
            self.send_json(
                event["type"],
                {"error": "Experiment and Expression fields required."},
                error=True)
            return

        try:
            qs = EquationTool(
                company=self.user.company,
                experiments=experiments,
                equations=expressions).evaluate()
        except ValueError as e:
            self.send_json(
                event["type"],
                {"error": str(e)},
                error=True)
            return

        try:
            data = list(qs)
        except DataError as e:
            self.send_json(
                event["type"],
                {"error": str(e)},
                error=True)
            return

        self.send_json(event["type"], {'uuid': event.get("uuid"), 'data':data})


    def fetch_projects(self, event):
        """
        Returns a list of projects. used for session creation.
        """
        qs = self.user.company.project_set()
        self.send_json(event["type"],
            ProjectSerializer(qs, many=True).data)

    def fetch_experiments(self, event):
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

        self.send_json(
            event["type"],
            ExperimentSerializer(qs, many=True).data)

    def fetch_fields(self, event):
        """
        Returns a set of fields in selected experiments.
        """
        experiments = event.get("experiments")

        fields_list = self.user.company.experimentdata_set \
            .filter(experiment_id__in = exFperiments) \
            .values('experimentData', flat=True)

        fields = reduce(lambda a, b: {**a, **b}, fields_list, {}).keys()

        self.send_json(event["type"], list(fields))

    def tool_save(self, event):
        """
        Saves a tool. If the id given is a string, then a new object is created
        else, tool is updated.
        """
        self.send_json(event["type"], {})