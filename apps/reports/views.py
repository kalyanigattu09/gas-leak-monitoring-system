from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.rooms.models import Room

from .services import PDFReportService


class SystemReportView(LoginRequiredMixin, View):
    def get(self, request):
        pdf = PDFReportService.generate_system_report()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="smart_gas_system_report.pdf"'
        return response


class RoomReportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        pdf = PDFReportService.generate_room_report(room)
        filename = f'smart_gas_report_{room.name.replace(" ", "_")}.pdf'
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
