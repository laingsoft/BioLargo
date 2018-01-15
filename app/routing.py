
from channels.routing import route
from .consumers import ws_analytics_columns, ws_index_page, ws_index_connect


analysis_routing = [
    route("websocket.receive", ws_analytics_columns, path=r"^/analysis/?$"),
    route("websocket.connect", ws_index_connect, path=r"^/?$"),
    route("websocket.receive", ws_index_page, path=r"^/?$")
    ]
