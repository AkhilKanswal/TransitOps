from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from vehicles.models import Vehicle
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    """
    ModelForm for scheduling and recording Fleet Vehicle Maintenance in TransitOps.
    Validates business rules for active status, cost ranges, and dates.
    """
    class Meta:
        model = Maintenance
        fields = [
            'vehicle',
            'issue_title',
            'description',
            'maintenance_type',
            'estimated_cost',
            'actual_cost',
            'start_date',
            'end_date',
            'assigned_technician',
            'status',
            'notes'
        ]
        widgets = {
            'issue_title': forms.TextInput(attrs={'placeholder': 'e.g. Brake Pad Replacement'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide details of the issue...'}),
            'estimated_cost': forms.NumberInput(attrs={'step': '0.01'}),
            'actual_cost': forms.NumberInput(attrs={'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_technician': forms.TextInput(attrs={'placeholder': 'e.g. John Doe'}),
            'status': forms.Select(),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs['class'] = classes

        # 1. Filter Vehicle Options: Only vehicles that are NOT retired
        if self.instance and self.instance.pk:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(
                ~Q(status=Vehicle.VehicleStatus.RETIRED) | Q(pk=self.instance.vehicle.pk)
            )
        else:
            self.fields['vehicle'].queryset = Vehicle.objects.exclude(status=Vehicle.VehicleStatus.RETIRED)

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        status = cleaned_data.get('status')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        estimated_cost = cleaned_data.get('estimated_cost')
        actual_cost = cleaned_data.get('actual_cost')

        # 2. Check for ONE active maintenance record per vehicle (Scheduled or In Progress)
        if vehicle and status in [Maintenance.MaintenanceStatus.SCHEDULED, Maintenance.MaintenanceStatus.IN_PROGRESS]:
            active_records = Maintenance.objects.filter(
                vehicle=vehicle,
                status__in=[Maintenance.MaintenanceStatus.SCHEDULED, Maintenance.MaintenanceStatus.IN_PROGRESS]
            )
            if self.instance and self.instance.pk:
                active_records = active_records.exclude(pk=self.instance.pk)

            if active_records.exists():
                error_msg = f"Vehicle {vehicle.registration_number} already has an active or scheduled maintenance record."
                self.add_error('vehicle', ValidationError(error_msg))
                self.add_error('status', ValidationError(error_msg))

        # 3. End Date cannot be earlier than Start Date
        if start_date and end_date:
            if end_date < start_date:
                self.add_error(
                    'end_date',
                    ValidationError("End date cannot be earlier than start date.")
                )

        # 4. Estimated Cost and Actual Cost cannot be negative
        if estimated_cost is not None and estimated_cost < 0:
            self.add_error('estimated_cost', ValidationError("Estimated cost cannot be negative."))

        if actual_cost is not None and actual_cost < 0:
            self.add_error('actual_cost', ValidationError("Actual cost cannot be negative."))

        return cleaned_data
