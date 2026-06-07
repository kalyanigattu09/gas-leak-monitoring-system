from django.contrib import admin
from django.db.models import Avg, Count, Max
from django.utils.html import format_html

from .models import Alert, AlertStatus, GasReading, GasStatus


@admin.register(GasReading)
class GasReadingAdmin(admin.ModelAdmin):
    list_display = ('room', 'gas_level', 'colored_status', 'timestamp')
    list_filter = ('status', 'room', 'timestamp')
    search_fields = ('room__name',)
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    @admin.display(description='Status')
    def colored_status(self, obj):
        colors = {
            GasStatus.SAFE: '#198754',
            GasStatus.WARNING: '#ffc107',
            GasStatus.DANGER: '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('room', 'level', 'status', 'short_message', 'timestamp')
    list_filter = ('status', 'room', 'timestamp')
    search_fields = ('room__name', 'message')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    actions = ['resolve_alerts']

    @admin.display(description='Message')
    def short_message(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message

    @admin.action(description='Mark selected alerts as resolved')
    def resolve_alerts(self, request, queryset):
        updated = queryset.filter(status=AlertStatus.ACTIVE).update(status=AlertStatus.RESOLVED)
        self.message_user(request, f'{updated} alert(s) marked as resolved.')


class MonitoringAdminSiteMixin:
    """Mixin for admin statistics — used in custom admin index."""

    @staticmethod
    def get_monitoring_stats():
        return {
            'total_readings': GasReading.objects.count(),
            'total_alerts': Alert.objects.count(),
            'active_alerts': Alert.objects.filter(status=AlertStatus.ACTIVE).count(),
            'peak_reading': GasReading.objects.aggregate(peak=Max('gas_level'))['peak'] or 0,
            'average_reading': round(
                GasReading.objects.aggregate(avg=Avg('gas_level'))['avg'] or 0, 1
            ),
            'readings_by_status': dict(
                GasReading.objects.values('status')
                .annotate(count=Count('id'))
                .values_list('status', 'count')
            ),
        }
