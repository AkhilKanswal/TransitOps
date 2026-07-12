from django.db import models
from vehicles.models import Vehicle

class Maintenance(models.Model):
    """
    Represents a vehicle maintenance record in the TransitOps fleet management system.
    """
    class MaintenanceType(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routine Service'
        REPAIR = 'REPAIR', 'Breakdown Repair'
        INSPECTION = 'INSPECTION', 'Safety Inspection'
        TYRES = 'TYRES', 'Tyre Service'

    class MaintenanceStatus(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenances',
        verbose_name="Vehicle",
        help_text="The fleet vehicle under maintenance. Automatically cascades on vehicle deletion."
    )
    issue_title = models.CharField(
        max_length=200,
        verbose_name="Issue Title",
        help_text="Brief summary of the issue (e.g., Brake pad replacement)."
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Detailed description of the maintenance activities/reasons."
    )
    maintenance_type = models.CharField(
        max_length=50,
        choices=MaintenanceType.choices,
        default=MaintenanceType.ROUTINE,
        verbose_name="Maintenance Type"
    )
    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Estimated Cost",
        help_text="Estimated cost for the service."
    )
    actual_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Actual Cost",
        help_text="Actual final cost incurred."
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        help_text="Date when the maintenance work commenced."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="End Date",
        help_text="Date when the maintenance was completed. Leave blank if ongoing."
    )
    assigned_technician = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Assigned Technician",
        help_text="Optional name of the technician performing the service."
    )
    status = models.CharField(
        max_length=20,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.SCHEDULED,
        verbose_name="Status"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Any additional remarks/notes about this service."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.issue_title} ({self.get_status_display()})"
