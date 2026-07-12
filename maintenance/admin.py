from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Maintenance model.
    """
    list_display = (
        'id',
        'vehicle',
        'issue_title',
        'maintenance_type',
        'estimated_cost',
        'actual_cost',
        'start_date',
        'end_date',
        'status'
    )
    list_filter = ('status', 'maintenance_type', 'start_date', 'end_date')
    search_fields = ('issue_title', 'description', 'vehicle__registration_number', 'assigned_technician')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
