from datetime import timedelta

from django.db.models import Avg, Count, Max
from django.utils import timezone

from apps.monitoring.models import Alert, GasReading
from apps.rooms.models import Room


class AnalyticsService:
    @staticmethod
    def get_summary():
        now = timezone.now()
        daily_start = now - timedelta(days=1)
        weekly_start = now - timedelta(days=7)
        monthly_start = now - timedelta(days=30)

        readings = GasReading.objects.all()

        daily_avg = readings.filter(timestamp__gte=daily_start).aggregate(avg=Avg('gas_level'))['avg']
        weekly_avg = readings.filter(timestamp__gte=weekly_start).aggregate(avg=Avg('gas_level'))['avg']
        monthly_avg = readings.filter(timestamp__gte=monthly_start).aggregate(avg=Avg('gas_level'))['avg']
        peak = readings.aggregate(peak=Max('gas_level'))['peak'] or 0

        room_comparison = []
        for room in Room.objects.all():
            stats = readings.filter(room=room).aggregate(
                average=Avg('gas_level'),
                peak=Max('gas_level'),
                count=Count('id'),
            )
            room_comparison.append({
                'room_id': room.id,
                'room_name': room.name,
                'average': round(stats['average'] or 0, 1),
                'peak': stats['peak'] or 0,
                'reading_count': stats['count'],
            })

        return {
            'daily_average': round(daily_avg or 0, 1),
            'weekly_average': round(weekly_avg or 0, 1),
            'monthly_average': round(monthly_avg or 0, 1),
            'peak_reading': peak,
            'alert_count': Alert.objects.count(),
            'total_readings': readings.count(),
            'room_comparison': room_comparison,
        }

    @staticmethod
    def get_chart_data():
        now = timezone.now()
        daily_labels = []
        daily_values = []
        for i in range(6, -1, -1):
            day = now - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            avg = GasReading.objects.filter(
                timestamp__gte=day_start,
                timestamp__lt=day_end,
            ).aggregate(avg=Avg('gas_level'))['avg']
            daily_labels.append(day_start.strftime('%a %d'))
            daily_values.append(round(avg or 0, 1))

        status_data = dict(
            GasReading.objects.values('status')
            .annotate(count=Count('id'))
            .values_list('status', 'count')
        )

        room_labels = []
        room_peaks = []
        for room in Room.objects.all():
            peak = GasReading.objects.filter(room=room).aggregate(peak=Max('gas_level'))['peak']
            room_labels.append(room.name)
            room_peaks.append(peak or 0)

        return {
            'line_chart': {'labels': daily_labels, 'values': daily_values},
            'pie_chart': {
                'labels': list(status_data.keys()),
                'values': list(status_data.values()),
            },
            'bar_chart': {'labels': room_labels, 'values': room_peaks},
        }
