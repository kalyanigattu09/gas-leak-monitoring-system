from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlertViewSet, AnalyticsViewSet, GasReadingViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'readings', GasReadingViewSet, basename='reading')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
