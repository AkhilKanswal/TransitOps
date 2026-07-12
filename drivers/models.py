from django.db import models

class Driver(models.Model):
    """
    Represents a vehicle driver in the TransitOps transport management system.
    """
    class DriverStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        ON_TRIP = 'ON_TRIP', 'On Trip'
        OFF_DUTY = 'OFF_DUTY', 'Off Duty'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    full_name = models.CharField(
        max_length=150,
        verbose_name="Full Name",
        help_text="Driver's full legal name."
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="License Number",
        help_text="Unique driver commercial driver license (CDL) number."
    )
    license_category = models.CharField(
        max_length=20,
        verbose_name="License Category",
        help_text="Class of commercial license (e.g., Heavy Motor Vehicle, Class A)."
    )
    license_expiry_date = models.DateField(
        verbose_name="License Expiry Date",
        help_text="Expiration date of driver's license."
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name="Contact Number",
        help_text="Primary phone/mobile contact number."
    )
    safety_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        verbose_name="Safety Score",
        help_text="Driver safety score rating out of 100.00."
    )
    status = models.CharField(
        max_length=20,
        choices=DriverStatus.choices,
        default=DriverStatus.AVAILABLE,
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['full_name']
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return f"{self.full_name} ({self.license_number})"
