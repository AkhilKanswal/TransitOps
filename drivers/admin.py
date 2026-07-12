from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """
    Administration configuration for the Driver model.
    """
    list_display = (
        'full_name',
        'license_number',
        'license_category',
        'license_expiry_date',
        'contact_number',
        'safety_score',
        'status'
    )
    list_filter = ('status', 'license_category')
    search_fields = ('full_name', 'license_number', 'contact_number')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')
