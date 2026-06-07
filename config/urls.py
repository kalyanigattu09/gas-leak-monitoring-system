from django.contrib import admin
from django.urls import include, path

import config.admin  # noqa: F401 — customize admin site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('rooms/', include('apps.rooms.urls')),
    path('monitoring/', include('apps.monitoring.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('reports/', include('apps.reports.urls')),
    path('api/v1/', include('apps.api.urls')),
]
