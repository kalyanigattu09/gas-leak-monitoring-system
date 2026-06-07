from django.urls import path

from .views import RoomReportView, SystemReportView

app_name = 'reports'

urlpatterns = [
    path('system/', SystemReportView.as_view(), name='system'),
    path('room/<int:pk>/', RoomReportView.as_view(), name='room'),
]
