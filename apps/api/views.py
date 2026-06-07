from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.analytics.services import AnalyticsService
from apps.monitoring.models import Alert, GasReading
from apps.monitoring.services.gas_service import DashboardService
from apps.rooms.models import Room

from .serializers import (
    AlertSerializer,
    AnalyticsSummarySerializer,
    DashboardStatsSerializer,
    GasReadingSerializer,
    RoomSerializer,
)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class GasReadingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GasReading.objects.select_related('room').all()
    serializer_class = GasReadingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['room', 'status']
    ordering_fields = ['timestamp', 'gas_level']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest = []
        for room in Room.objects.all():
            reading = room.latest_reading
            if reading:
                latest.append(GasReadingSerializer(reading).data)
        return Response(latest)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related('room').all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['room', 'status']
    ordering_fields = ['timestamp', 'level']

    http_method_names = ['get', 'head', 'options', 'patch']


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = AnalyticsService.get_summary()
        serializer = AnalyticsSummarySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def charts(self, request):
        return Response(AnalyticsService.get_chart_data())

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        data = DashboardService.get_dashboard_context()
        payload = {
            'total_rooms': data['total_rooms'],
            'total_alerts': data['total_alerts'],
            'peak_reading': data['peak_reading'],
            'average_reading': data['average_reading'],
            'status_counts': data['status_counts'],
        }
        serializer = DashboardStatsSerializer(payload)
        return Response(serializer.data)
