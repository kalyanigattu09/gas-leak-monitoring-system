import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services import AnalyticsService


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        summary = AnalyticsService.get_summary()
        charts = AnalyticsService.get_chart_data()
        context['summary'] = summary
        context['line_chart_json'] = json.dumps(charts['line_chart'])
        context['pie_chart_json'] = json.dumps(charts['pie_chart'])
        context['bar_chart_json'] = json.dumps(charts['bar_chart'])
        return context
