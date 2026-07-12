from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Trip model.
    """
    list_display = (
        'id',
        'vehicle',
        'driver',
        'source',
        'destination',
        'cargo_weight',
        'planned_distance',
        'revenue',
        'status',
        'start_date',
        'end_date',
        'created_at'
    )
    list_filter = ('status', 'start_date', 'end_date', 'created_at')
    search_fields = (
        'source',
        'destination',
        'vehicle__registration_number',
        'driver__full_name',
        'driver__license_number'
    )
    ordering = ('-created_at',)
    readonly_fields = ('start_date', 'end_date', 'created_at', 'updated_at')
