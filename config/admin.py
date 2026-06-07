from django.contrib import admin
from django.db.models import Avg, Max

from apps.monitoring.admin import MonitoringAdminSiteMixin

admin.site.site_header = 'Smart Gas Monitoring Admin'
admin.site.site_title = 'Smart Gas Admin'
admin.site.index_title = 'System Administration'


def get_admin_stats():
    return MonitoringAdminSiteMixin.get_monitoring_stats()


original_index = admin.site.index


def custom_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context['monitoring_stats'] = get_admin_stats()
    return original_index(request, extra_context)


admin.site.index = custom_index
