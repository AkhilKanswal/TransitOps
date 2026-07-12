from django.db import models
from vehicles.models import Vehicle

class Maintenance(models.Model):
    """
    Represents a vehicle maintenance record in the TransitOps fleet management system.
    """
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenances',
        verbose_name="Vehicle",
        help_text="The fleet vehicle under maintenance. Automatically cascades on vehicle deletion."
    )
    issue = models.CharField(
        max_length=200,
        verbose_name="Issue",
        help_text="Brief summary of the issue (e.g., Engine Tune-up, Oil Change)."
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Detailed description of the maintenance activities/reasons."
    )
    maintenance_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Maintenance Cost",
        help_text="Cost incurred for the maintenance service."
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
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Designates whether this maintenance task is currently active/ongoing."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"

    def __str__(self):
        status_str = "Ongoing" if self.is_active else "Completed"
        return f"{self.vehicle.registration_number} - {self.issue} ({status_str})"
