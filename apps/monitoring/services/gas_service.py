import logging
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models import Avg, Max
from django.utils import timezone

from apps.rooms.models import Room

from ..models import Alert, AlertStatus, GasReading, GasStatus, evaluate_gas_status
from .email_service import send_danger_alert_email

logger = logging.getLogger(__name__)


class GasSimulationService:
    """Generates simulated gas readings and triggers alerts."""

    def __init__(self):
        self.danger_threshold = getattr(settings, 'GAS_LEVEL_WARNING_MAX', 70)
        self.max_level = getattr(settings, 'GAS_LEVEL_DANGER_MAX', 100)

    def generate_gas_level(self) -> int:
        return random.randint(0, self.max_level)

    def process_room(self, room: Room) -> GasReading:
        gas_level = self.generate_gas_level()
        status = evaluate_gas_status(gas_level)

        reading = GasReading.objects.create(
            room=room,
            gas_level=gas_level,
            status=status,
        )

        alert = None
        if gas_level > self.danger_threshold:
            alert = self._create_alert(room, gas_level, status)
            send_danger_alert_email(alert)

        self._broadcast_update(reading, alert)
        return reading

    def process_all_rooms(self) -> list[GasReading]:
        rooms = Room.objects.all()
        if not rooms.exists():
            logger.warning('No rooms found. Create rooms before running simulation.')
            return []
        return [self.process_room(room) for room in rooms]

    def _create_alert(self, room: Room, gas_level: int, status: str) -> Alert:
        message = (
            f'DANGER: Gas level {gas_level} detected in {room.name}. '
            f'Status: {status}. Immediate action required.'
        )
        return Alert.objects.create(
            room=room,
            level=gas_level,
            message=message,
            status=AlertStatus.ACTIVE,
        )

    def _broadcast_update(self, reading: GasReading, alert: Alert | None) -> None:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return

        payload = {
            'type': 'gas_update',
            'reading': {
                'room_id': reading.room_id,
                'room_name': reading.room.name,
                'gas_level': reading.gas_level,
                'status': reading.status,
                'timestamp': reading.timestamp.isoformat(),
            },
        }
        if alert:
            payload['alert'] = {
                'id': alert.id,
                'room_id': alert.room_id,
                'room_name': alert.room.name,
                'level': alert.level,
                'message': alert.message,
                'status': alert.status,
                'timestamp': alert.timestamp.isoformat(),
            }

        async_to_sync(channel_layer.group_send)('gas_monitoring', payload)


class DashboardService:
    """Aggregates statistics for the monitoring dashboard."""

    @staticmethod
    def get_dashboard_context() -> dict:
        rooms = Room.objects.prefetch_related('gas_readings').all()
        total_rooms = rooms.count()
        total_alerts = Alert.objects.filter(status=AlertStatus.ACTIVE).count()

        latest_readings = []
        for room in rooms:
            reading = room.latest_reading
            latest_readings.append({
                'room': room,
                'reading': reading,
                'gas_level': reading.gas_level if reading else None,
                'status': reading.status if reading else 'UNKNOWN',
            })

        reading_stats = GasReading.objects.aggregate(
            peak=Max('gas_level'),
            average=Avg('gas_level'),
        )

        status_counts = {
            'SAFE': GasReading.objects.filter(status=GasStatus.SAFE).count(),
            'WARNING': GasReading.objects.filter(status=GasStatus.WARNING).count(),
            'DANGER': GasReading.objects.filter(status=GasStatus.DANGER).count(),
        }

        recent_alerts = Alert.objects.select_related('room').order_by('-timestamp')[:10]

        return {
            'total_rooms': total_rooms,
            'total_alerts': total_alerts,
            'peak_reading': reading_stats['peak'] or 0,
            'average_reading': round(reading_stats['average'] or 0, 1),
            'room_readings': latest_readings,
            'status_counts': status_counts,
            'recent_alerts': recent_alerts,
            'last_updated': timezone.now(),
        }
