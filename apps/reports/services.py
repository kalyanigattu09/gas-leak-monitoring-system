from datetime import datetime
from io import BytesIO

from django.db.models import Avg, Count, Max
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.monitoring.models import Alert, AlertStatus, GasReading
from apps.rooms.models import Room


class PDFReportService:
    @staticmethod
    def generate_room_report(room: Room) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.HexColor('#0d6efd'),
        )
        elements = []

        elements.append(Paragraph('Smart Gas Monitoring Report', title_style))
        elements.append(Paragraph(f'Room: {room.name}', styles['Heading2']))
        elements.append(Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph('Room Information', styles['Heading3']))
        room_info = [
            ['Field', 'Value'],
            ['Name', room.name],
            ['Description', room.description or 'N/A'],
            ['Created', room.created_at.strftime('%Y-%m-%d %H:%M')],
            ['Current Level', str(room.current_gas_level or 'N/A')],
            ['Current Status', room.current_status],
        ]
        elements.append(PDFReportService._make_table(room_info))
        elements.append(Spacer(1, 0.3 * inch))

        readings = GasReading.objects.filter(room=room)
        stats = readings.aggregate(
            average=Avg('gas_level'),
            peak=Max('gas_level'),
            count=Count('id'),
        )
        elements.append(Paragraph('Gas Statistics', styles['Heading3']))
        stats_data = [
            ['Metric', 'Value'],
            ['Total Readings', str(stats['count'])],
            ['Average Level', f"{round(stats['average'] or 0, 1)}"],
            ['Peak Level', str(stats['peak'] or 0)],
        ]
        elements.append(PDFReportService._make_table(stats_data))
        elements.append(Spacer(1, 0.3 * inch))

        alert_qs = Alert.objects.filter(room=room)
        alerts = list(alert_qs.order_by('-timestamp')[:20])
        elements.append(Paragraph('Alert History (Last 20)', styles['Heading3']))
        if alerts:
            alert_data = [['Timestamp', 'Level', 'Status', 'Message']]
            for alert in alerts:
                alert_data.append([
                    alert.timestamp.strftime('%Y-%m-%d %H:%M'),
                    str(alert.level),
                    alert.status,
                    alert.message[:50] + '...' if len(alert.message) > 50 else alert.message,
                ])
            elements.append(PDFReportService._make_table(alert_data, col_widths=[1.3 * inch, 0.7 * inch, 0.8 * inch, 3.2 * inch]))
        else:
            elements.append(Paragraph('No alerts recorded for this room.', styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        active_alerts = alert_qs.filter(status=AlertStatus.ACTIVE).count()
        danger_readings = readings.filter(status='DANGER').count()
        elements.append(Paragraph('Incident Summary', styles['Heading3']))
        summary_data = [
            ['Metric', 'Value'],
            ['Active Alerts', str(active_alerts)],
            ['Danger Readings', str(danger_readings)],
            ['Total Alerts', str(alert_qs.count())],
        ]
        elements.append(PDFReportService._make_table(summary_data))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def generate_system_report() -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph('Smart Gas System Report', styles['Heading1']),
            Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']),
            Spacer(1, 0.3 * inch),
        ]

        stats = GasReading.objects.aggregate(avg=Avg('gas_level'), peak=Max('gas_level'), count=Count('id'))
        summary = [
            ['Metric', 'Value'],
            ['Total Rooms', str(Room.objects.count())],
            ['Total Readings', str(stats['count'])],
            ['Average Level', f"{round(stats['avg'] or 0, 1)}"],
            ['Peak Level', str(stats['peak'] or 0)],
            ['Total Alerts', str(Alert.objects.count())],
            ['Active Alerts', str(Alert.objects.filter(status=AlertStatus.ACTIVE).count())],
        ]
        elements.append(Paragraph('System Overview', styles['Heading2']))
        elements.append(PDFReportService._make_table(summary))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _make_table(data, col_widths=None):
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        return table
