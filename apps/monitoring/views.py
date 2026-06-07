from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Alert, AlertStatus
from .services.gas_service import DashboardService


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'monitoring/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DashboardService.get_dashboard_context())
        return context


class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = 'monitoring/alert_list.html'
    context_object_name = 'alerts'
    paginate_by = 20

    def get_queryset(self):
        return Alert.objects.select_related('room').order_by('-timestamp')


class AlertResolveView(LoginRequiredMixin, View):
    success_url = reverse_lazy('monitoring:alerts')

    def post(self, request, pk):
        alert = get_object_or_404(Alert, pk=pk, status=AlertStatus.ACTIVE)
        alert.status = AlertStatus.RESOLVED
        alert.save(update_fields=['status'])
        messages.success(request, 'Alert marked as resolved.')
        return redirect(self.success_url)
