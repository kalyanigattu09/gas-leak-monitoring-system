from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RoomForm
from .models import Room


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:list')

    def form_valid(self, form):
        messages.success(self.request, f'Room "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:list')

    def form_valid(self, form):
        messages.success(self.request, f'Room "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:list')

    def form_valid(self, form):
        messages.success(self.request, f'Room "{self.object.name}" deleted successfully.')
        return super().form_valid(form)
