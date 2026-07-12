from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Vehicle model.
    """
    list_display = (
        'registration_number',
        'model_name',
        'vehicle_type',
        'max_load_capacity',
        'current_odometer',
        'status',
        'created_at'
    )
    list_filter = ('status', 'vehicle_type')
    search_fields = ('registration_number', 'model_name', 'vehicle_type')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
