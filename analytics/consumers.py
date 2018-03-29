from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Session, Action
import analytics.base_analysis as tools
from functools import reduce

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
        self.qs = self.user.company.experimentdata_set.all()

        if self.user.is_anonymous:
            self.close()

        self.accept()

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Arguments:  content - decoded JSON (a dictionary)
        """
        action = content.get('action')

        if action == 'get_tags':
            self.get_tags()

            return

        field = content.get('field')

        val = TOOLS[action](self.user.company.experimentdata_set.all(), field).evaluate()

        self.send_json(val)

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
        fields_list = self.qs.experimentdata_set.all().values_list('experimentData', flat=True)
        fields = reduce(lambda a, b: {**a, **b}, fields_list).keys()

        self.send_json({'fields': fields})
