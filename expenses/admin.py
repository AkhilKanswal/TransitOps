from django.contrib import admin
from .models import Expense, FuelLog

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Expense model.
    """
    list_display = (
        'id',
        'vehicle',
        'trip',
        'expense_type',
        'amount',
        'expense_date'
    )
    list_filter = ('expense_type', 'expense_date')
    search_fields = ('remarks', 'vehicle__registration_number', 'trip__source', 'trip__destination')
    ordering = ('-expense_date',)


@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    """
    Administration configuration for the FuelLog model.
    """
    list_display = (
        'id',
        'vehicle',
        'trip',
        'fuel_liters',
        'fuel_cost',
        'log_date'
    )
    list_filter = ('log_date',)
    search_fields = ('vehicle__registration_number', 'trip__source', 'trip__destination')
    ordering = ('-log_date',)
