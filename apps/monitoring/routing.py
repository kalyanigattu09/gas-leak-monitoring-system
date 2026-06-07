from django.urls import path

from .consumers import GasMonitoringConsumer

websocket_urlpatterns = [
    path('ws/gas/', GasMonitoringConsumer.as_asgi()),
]
