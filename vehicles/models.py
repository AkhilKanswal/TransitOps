from django.db import models

class Vehicle(models.Model):
    """
    Represents a fleet vehicle in the TransitOps transport management system.
    """
    class VehicleStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        ON_TRIP = 'ON_TRIP', 'On Trip'
        IN_SHOP = 'IN_SHOP', 'In Shop'
        RETIRED = 'RETIRED', 'Retired'

    registration_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Registration Number",
        help_text="Unique vehicle registration plate/number."
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name="Model Name",
        help_text="Model and manufacturer (e.g., Tata Prima 4025.S)."
    )
    vehicle_type = models.CharField(
        max_length=50,
        verbose_name="Vehicle Type",
        help_text="Type of vehicle (e.g., Heavy Duty Truck, Cargo Van)."
    )
    max_load_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Max Load Capacity (kg)",
        help_text="Maximum load capacity in kilograms (kg)."
    )
    current_odometer = models.PositiveIntegerField(
        default=0,
        verbose_name="Current Odometer (km)",
        help_text="Current odometer reading in kilometers."
    )
    acquisition_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Acquisition Cost",
        help_text="Cost incurred during vehicle acquisition."
    )
    status = models.CharField(
        max_length=20,
        choices=VehicleStatus.choices,
        default=VehicleStatus.AVAILABLE,
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.registration_number} - {self.model_name}"
