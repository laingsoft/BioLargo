
from channels.routing import route, include
from app.consumers import ws_analytics_columns
channel_routing = [
    include('app.routing.analysis_routing', path=r"^/app")
]
