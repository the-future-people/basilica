import uuid
from django.db import models


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    class PaymentMethod(models.TextChoices):
        MTN_MOMO = 'mtn_momo', 'MTN Mobile Money'
        VODAFONE_CASH = 'vodafone_cash', 'Vodafone Cash'
        AIRTELTIGO_MONEY = 'airteltigo_money', 'AirtelTigo Money'
        CASH = 'cash', 'Cash'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'

    class PaymentType(models.TextChoices):
        SUBSCRIPTION = 'subscription', 'Monthly Subscription'
        BIN_CONTRIBUTION = 'bin_contribution', 'Bin Contribution'
        PENALTY = 'penalty', 'Penalty Fee'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        'billing.Subscription',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    # Mobile Money specific
    momo_number = models.CharField(max_length=20, blank=True)
    momo_transaction_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    momo_network = models.CharField(max_length=50, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    failure_reason = models.TextField(blank=True)

    # Billing period this payment covers
    billing_period_start = models.DateField(null=True, blank=True)
    billing_period_end = models.DateField(null=True, blank=True)

    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-initiated_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['subscription', '-initiated_at']),
            models.Index(fields=['status', '-initiated_at']),
        ]

    def __str__(self):
        return f"{self.subscription.customer_name} - GHS {self.amount} - {self.status}"