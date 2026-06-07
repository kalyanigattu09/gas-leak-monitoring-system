import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_danger_alert_email(alert) -> bool:
    """
    Send email notification when gas level exceeds danger threshold.
    Uses console backend in development by default.
    """
    subject = f'[DANGER] Gas Alert — {alert.room.name} (Level {alert.level})'

    context = {
        'alert': alert,
        'room_name': alert.room.name,
        'gas_level': alert.level,
        'status': 'DANGER',
        'timestamp': alert.timestamp,
        'message': alert.message,
    }

    html_message = render_to_string('emails/danger_alert.html', context)
    plain_message = render_to_string('emails/danger_alert.txt', context)

    recipient_list = _get_recipient_list()

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info('Danger alert email sent for room %s', alert.room.name)
        return True
    except Exception:
        logger.exception('Failed to send danger alert email for room %s', alert.room.name)
        return False


def _get_recipient_list() -> list[str]:
    admin_email = getattr(settings, 'ALERT_ADMIN_EMAIL', '')
    if admin_email:
        return [admin_email]

    from django.contrib.auth.models import User
    staff_emails = list(
        User.objects.filter(is_staff=True, is_active=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )
    if staff_emails:
        return staff_emails

    return [settings.DEFAULT_FROM_EMAIL.split('<')[-1].rstrip('>').strip()]
