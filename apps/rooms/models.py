from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def latest_reading(self):
        return self.gas_readings.order_by('-timestamp').first()

    @property
    def current_status(self):
        reading = self.latest_reading
        return reading.status if reading else 'UNKNOWN'

    @property
    def current_gas_level(self):
        reading = self.latest_reading
        return reading.gas_level if reading else None
