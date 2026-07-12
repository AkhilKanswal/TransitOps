from django.db import models
from vehicles.models import Vehicle
from trips.models import Trip

class Expense(models.Model):
    """
    Represents an operational expense incurred during fleet transit in TransitOps.
    """
    class ExpenseType(models.TextChoices):
        TOLLS = 'TOLLS', 'Tolls'
        DRIVER_ALLOWANCE = 'DRIVER_ALLOWANCE', 'Driver Allowance'
        PERMITS = 'PERMITS', 'Permits & Fines'
        MEALS = 'MEALS', 'Meals & Lodging'
        MISC = 'MISC', 'Miscellaneous'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name="Vehicle",
        help_text="The vehicle associated with this expense. Cascades on deletion."
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name="Trip",
        help_text="The operational trip during which the expense was incurred. Kept as null if trip is deleted."
    )
    expense_type = models.CharField(
        max_length=50,
        choices=ExpenseType.choices,
        default=ExpenseType.MISC,
        verbose_name="Expense Type"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Financial amount of the expense."
    )
    expense_date = models.DateField(
        verbose_name="Expense Date",
        help_text="The date when the expense occurred."
    )
    remarks = models.TextField(
        blank=True,
        verbose_name="Remarks",
        help_text="Any additional description or justification for the expense."
    )

    class Meta:
        ordering = ['-expense_date']
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.get_expense_type_display()} - {self.amount} ({self.expense_date})"


class FuelLog(models.Model):
    """
    Represents a fuel refuel record logged for a vehicle in TransitOps.
    """
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='fuel_logs',
        verbose_name="Vehicle",
        help_text="The vehicle being refueled. Cascades on deletion."
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fuel_logs',
        verbose_name="Trip",
        help_text="The trip during which the refueling occurred. Kept as null if trip is deleted."
    )
    fuel_liters = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Fuel (Liters)",
        help_text="Volume of fuel purchased in liters."
    )
    fuel_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Fuel Cost",
        help_text="Total cost of the purchased fuel."
    )
    log_date = models.DateField(
        verbose_name="Log Date",
        help_text="The date when fuel was logged."
    )

    class Meta:
        ordering = ['-log_date']
        verbose_name = "Fuel Log"
        verbose_name_plural = "Fuel Logs"

    def __str__(self):
        return f"Fuel for {self.vehicle.registration_number} - {self.fuel_liters}L ({self.log_date})"
