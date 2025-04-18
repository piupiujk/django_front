import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from docanalyser.proxy_app.middleware import AsyncPrometheusMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docanalyser.settings')

application = ProtocolTypeRouter({
    "http": AsyncPrometheusMiddleware(get_asgi_application()),
    "websocket": URLRouter([]),
})