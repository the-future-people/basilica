import uuid
from django.db import models


class Subscription(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'
        CANCELLED = 'cancelled', 'Cancelled'

    class CustomerType(models.TextChoices):
        HOUSEHOLD = 'household', 'Household'
        BUSINESS = 'business', 'Business'
        GOVERNMENT = 'government', 'Government'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Customer info
    customer_name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, choices=CustomerType.choices, default=CustomerType.HOUSEHOLD)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    # Linked bin
    bin = models.OneToOneField(
        'bins.Bin',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    # Pricing
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Full monthly fee in GHS")
    bin_contribution = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly bin cost contribution in GHS")

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    # Billing cycle
    billing_day = models.PositiveSmallIntegerField(default=1, help_text="Day of month billing is due")
    next_billing_date = models.DateField()

    # Timestamps
    started_at = models.DateField()
    cancelled_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.customer_name} - {self.bin} - {self.status}"

    @property
    def total_monthly_charge(self):
        return self.monthly_fee + self.bin_contribution