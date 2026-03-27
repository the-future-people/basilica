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
    location_description = models.CharField(max_length=255)
    circuit = models.ForeignKey(
        'circuits.Circuit',
        on_delete=models.SET_NULL,
        null=True,
        related_name='bins'
    )

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