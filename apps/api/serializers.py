from rest_framework import serializers

from apps.monitoring.models import Alert, GasReading
from apps.rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    current_gas_level = serializers.IntegerField(read_only=True)
    current_status = serializers.CharField(read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'created_at', 'current_gas_level', 'current_status')
        read_only_fields = ('created_at',)


class GasReadingSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = GasReading
        fields = ('id', 'room', 'room_name', 'gas_level', 'status', 'timestamp')
        read_only_fields = ('status', 'timestamp')


class AlertSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Alert
        fields = ('id', 'room', 'room_name', 'level', 'message', 'status', 'timestamp')
        read_only_fields = ('message', 'timestamp')


class AnalyticsSummarySerializer(serializers.Serializer):
    daily_average = serializers.FloatField()
    weekly_average = serializers.FloatField()
    monthly_average = serializers.FloatField()
    peak_reading = serializers.IntegerField()
    alert_count = serializers.IntegerField()
    total_readings = serializers.IntegerField()
    room_comparison = serializers.ListField()


class DashboardStatsSerializer(serializers.Serializer):
    total_rooms = serializers.IntegerField()
    total_alerts = serializers.IntegerField()
    peak_reading = serializers.IntegerField()
    average_reading = serializers.FloatField()
    status_counts = serializers.DictField()
