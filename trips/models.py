from django.db import models
from vehicles.models import Vehicle
from drivers.models import Driver

class Trip(models.Model):
    """
    Represents an operational trip dispatched with a vehicle and a driver in TransitOps.
    """
    class TripStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        DISPATCHED = 'DISPATCHED', 'Dispatched'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name='trips',
        verbose_name="Vehicle",
        help_text="The fleet vehicle assigned to this trip. Protected from accidental deletion."
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name='trips',
        verbose_name="Driver",
        help_text="The driver assigned to this trip. Protected from accidental deletion."
    )
    source = models.CharField(
        max_length=255,
        verbose_name="Source",
        help_text="Starting location of the trip."
    )
    destination = models.CharField(
        max_length=255,
        verbose_name="Destination",
        help_text="Destination location of the trip."
    )
    cargo_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cargo Weight (kg)",
        help_text="Weight of the transported cargo in kilograms."
    )
    planned_distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Planned Distance (km)",
        help_text="Estimated trip distance in kilometers."
    )
    revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Revenue",
        help_text="Total revenue generated from the trip."
    )
    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.DRAFT,
        verbose_name="Status"
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Start Date",
        help_text="Date and time when the trip was dispatched."
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="End Date",
        help_text="Date and time when the trip was completed."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def __str__(self):
        return f"Trip #{self.id or 'Draft'}: {self.source} to {self.destination}"
