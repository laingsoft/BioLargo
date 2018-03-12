
from channels.routing import route, include

channel_routing = [
    include('app.routing.analysis_routing', path=r"^/app")
]
