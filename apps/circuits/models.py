import uuid
from django.db import models


class Circuit(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="e.g. Accra Circuit 1")
    code = models.CharField(max_length=20, unique=True, help_text="e.g. ACC-001")
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    # Geographic center of the circuit
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Circuit'
        verbose_name_plural = 'Circuits'

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def total_bins(self):
        return self.bins.count()

    @property
    def active_bins(self):
        return self.bins.filter(status='active').count()