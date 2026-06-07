from django.urls import path

from .views import RoomCreateView, RoomDeleteView, RoomListView, RoomUpdateView

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='list'),
    path('add/', RoomCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', RoomUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', RoomDeleteView.as_view(), name='delete'),
]
