
from channels.routing import route
from .consumers import ws_index_page, ws_index_connect


analysis_routing = [
    route("websocket.connect", ws_index_connect, path=r"^/?$"),
    route("websocket.receive", ws_index_page, path=r"^/?$")
    ]
