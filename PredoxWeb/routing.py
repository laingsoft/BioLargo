from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import app.routing
import analytics.routing
from django.conf.urls import url, include

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url('app/', include(app.routing.websocket_urlpatterns)),
            url('analytics/', include(analytics.routing.websocket_urlpatterns)),
        ])
    ),
})
