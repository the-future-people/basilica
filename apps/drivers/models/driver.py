import uuid
from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='driver_profile'
    )
    circuit = models.ForeignKey(
        'circuits.Circuit',
        on_delete=models.SET_NULL,
        null=True,
        related_name='drivers'
    )

    # Personal info
    phone_number = models.CharField(max_length=20, unique=True)
    ghana_card_number = models.CharField(max_length=50, unique=True)
    profile_photo = models.ImageField(upload_to='drivers/photos/', null=True, blank=True)

    # Security — device binding
    registered_device_id = models.CharField(max_length=255, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_active_at = models.DateTimeField(null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_on_trip = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.circuit}"