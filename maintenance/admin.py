from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Maintenance model.
    """
    list_display = (
        'vehicle',
        'issue',
        'maintenance_cost',
        'start_date',
        'end_date',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('issue', 'description', 'vehicle__registration_number')
    ordering = ('-start_date',)
    readonly_fields = ('created_at',)
