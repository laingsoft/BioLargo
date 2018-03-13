from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing
import analytics.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            app.routing.websocket_urlpatterns,
            analytics.routing.websocket_urlpatterns
        ])
    ),
})
