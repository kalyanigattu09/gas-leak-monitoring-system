from django.conf import settings
from django.db import models


class GasStatus(models.TextChoices):
    SAFE = 'SAFE', 'Safe'
    WARNING = 'WARNING', 'Warning'
    DANGER = 'DANGER', 'Danger'


class AlertStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    RESOLVED = 'RESOLVED', 'Resolved'


class GasReading(models.Model):
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE,
        related_name='gas_readings',
    )
    gas_level = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=10, choices=GasStatus.choices)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['room', '-timestamp']),
            models.Index(fields=['status', '-timestamp']),
        ]

    def __str__(self):
        return f'{self.room.name}: {self.gas_level} ({self.status})'


class Alert(models.Model):
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE,
        related_name='alerts',
    )
    level = models.PositiveSmallIntegerField()
    message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=AlertStatus.choices,
        default=AlertStatus.ACTIVE,
    )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['status', '-timestamp']),
            models.Index(fields=['room', '-timestamp']),
        ]

    def __str__(self):
        return f'Alert: {self.room.name} — Level {self.level}'


def evaluate_gas_status(gas_level: int) -> str:
    """Categorize gas level into SAFE, WARNING, or DANGER."""
    safe_max = getattr(settings, 'GAS_LEVEL_SAFE_MAX', 40)
    warning_max = getattr(settings, 'GAS_LEVEL_WARNING_MAX', 70)

    if gas_level <= safe_max:
        return GasStatus.SAFE
    if gas_level <= warning_max:
        return GasStatus.WARNING
    return GasStatus.DANGER
