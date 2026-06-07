from django.urls import path

from .views import AlertListView, AlertResolveView, DashboardView

app_name = 'monitoring'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('alerts/', AlertListView.as_view(), name='alerts'),
    path('alerts/<int:pk>/resolve/', AlertResolveView.as_view(), name='alert_resolve'),
]
