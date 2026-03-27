import uuid
from django.db import models


class Bin(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        MAINTENANCE = 'maintenance', 'Maintenance'
        DAMAGED = 'damaged', 'Damaged'

    class BinType(models.TextChoices):
        GENERAL = 'general', 'General Waste'
        RECYCLABLE = 'recyclable', 'Recyclable'
        ORGANIC = 'organic', 'Organic'

    # Identity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_eui = models.CharField(max_length=16, unique=True, help_text="LoRaWAN Device EUI")
    serial_number = models.CharField(max_length=100, unique=True)
    bin_type = models.CharField(max_length=20, choices=BinType.choices, default=BinType.GENERAL)

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_description = models.CharField(max_length=255, help_text="e.g. In front of Accra Mall gate")
    circuit = models.ForeignKey('circuits.Circuit', on_delete=models.SET_NULL, null=True, related_name='bins')

    # Physical specs
    capacity_litres = models.PositiveIntegerField(default=120)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bin'
        verbose_name_plural = 'Bins'

    def __str__(self):
        return f"Bin {self.serial_number} - {self.location_description}"

    @property
    def latest_telemetry(self):
        return self.telemetry_records.order_by('-recorded_at').first()

    @property
    def fill_level(self):
        telemetry = self.latest_telemetry
        return telemetry.fill_level if telemetry else None


class BinTelemetry(models.Model):
    """
    Every data ping from a bin is stored here.
    This is the raw time-series data from the field.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='telemetry_records')

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