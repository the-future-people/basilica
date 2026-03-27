import uuid
from django.db import models


class Trip(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(
        'drivers.Driver',
        on_delete=models.CASCADE,
        related_name='trips'
    )
    circuit = models.ForeignKey(
        'circuits.Circuit',
        on_delete=models.CASCADE,
        related_name='trips'
    )

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Timing
    scheduled_date = models.DateField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Stats
    total_bins_planned = models.PositiveIntegerField(default=0)
    total_bins_collected = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'

    def __str__(self):
        return f"Trip {self.id} - {self.driver} - {self.scheduled_date}"

    @property
    def completion_rate(self):
        if self.total_bins_planned == 0:
            return 0
        return round((self.total_bins_collected / self.total_bins_planned) * 100, 1)


class TripStop(models.Model):
    """Each bin stop within a trip."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COLLECTED = 'collected', 'Collected'
        SKIPPED = 'skipped', 'Skipped'
        REPORTED = 'reported', 'Reported Issue'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    bin = models.ForeignKey('bins.Bin', on_delete=models.CASCADE, related_name='trip_stops')

    # Order in the route
    order = models.PositiveIntegerField()

    # Snapshot of fill level when route was generated
    fill_level_at_dispatch = models.PositiveSmallIntegerField(null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    collected_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Trip Stop'
        verbose_name_plural = 'Trip Stops'
        unique_together = ['trip', 'bin']

    def __str__(self):
        return f"Stop {self.order} - {self.bin.serial_number} - {self.status}"