
from channels.routing import route
from app.consumers import ws_analytics_columns

channel_routing = [
    route("websocket.receive", ws_analytics_columns),
]
