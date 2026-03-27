import uuid
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        # Bin alerts
        BIN_FULL = 'bin_full', 'Bin Full'
        BIN_TAMPERED = 'bin_tampered', 'Bin Tampered'
        BIN_OFFLINE = 'bin_offline', 'Bin Offline'
        BIN_LOW_BATTERY = 'bin_low_battery', 'Bin Low Battery'
        # Trip alerts
        TRIP_STARTED = 'trip_started', 'Trip Started'
        TRIP_COMPLETED = 'trip_completed', 'Trip Completed'
        TRIP_OVERDUE = 'trip_overdue', 'Trip Overdue'
        # Billing alerts
        PAYMENT_DUE = 'payment_due', 'Payment Due'
        PAYMENT_SUCCESS = 'payment_success', 'Payment Successful'
        PAYMENT_FAILED = 'payment_failed', 'Payment Failed'
        # System alerts
        DRIVER_ANOMALY = 'driver_anomaly', 'Driver Location Anomaly'
        SYSTEM_ALERT = 'system_alert', 'System Alert'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    class Channel(models.TextChoices):
        IN_APP = 'in_app', 'In App'
        SMS = 'sms', 'SMS'
        EMAIL = 'email', 'Email'
        PUSH = 'push', 'Push Notification'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Recipient
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # Notification details
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    title = models.CharField(max_length=255)
    message = models.TextField()

    # Linked objects — all optional depending on notification type
    bin = models.ForeignKey(
        'bins.Bin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    trip = models.ForeignKey(
        'drivers.Trip',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    payment = models.ForeignKey(
        'billing.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )

    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type', '-created_at']),
            models.Index(fields=['priority', 'is_sent']),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username} - {self.created_at}"