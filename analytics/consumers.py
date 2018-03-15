from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


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

        self.accept()

    def receive_json(self, content):
        """
        Called when a text frame is received.
        Arguments:  content - decoded JSON (a dictionary)
        """
        self.send_json(content)

    def disconnect(self, code):
        """
        Called when websocket connetion is closed.
        """
        pass
