import uuid
from django.db import models


class BinTelemetry(models.Model):
    """
    Every data ping from a bin is stored here.
    Raw time-series data from the field.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bin = models.ForeignKey(
        'bins.Bin',
        on_delete=models.CASCADE,
        related_name='telemetry_records'
    )

    # Sensor data
    fill_level = models.PositiveSmallIntegerField(help_text="Fill percentage 0-100")
    battery_level = models.PositiveSmallIntegerField(help_text="Battery percentage 0-100")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_tampered = models.BooleanField(default=False)
    signal_strength = models.IntegerField(null=True, blank=True, help_text="RSSI in dBm")

    # Meta
    recorded_at = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Bin Telemetry'
        verbose_name_plural = 'Bin Telemetry Records'
        indexes = [
            models.Index(fields=['bin', '-recorded_at']),
        ]

    def __str__(self):
        return f"{self.bin.serial_number} - {self.fill_level}% @ {self.recorded_at}"