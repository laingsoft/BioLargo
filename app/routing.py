
from channels.routing import route
from .consumers import ws_analytics_columns


analysis_routing = [
    route("websocket.receive", ws_analytics_columns, path=r"^/analysis/?$"),
    ]
