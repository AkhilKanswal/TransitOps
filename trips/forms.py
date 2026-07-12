import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from vehicles.models import Vehicle
from drivers.models import Driver
from .models import Trip

class TripForm(forms.ModelForm):
    """
    ModelForm for creating and editing operational Trips in TransitOps.
    Filters available vehicles/drivers and validates business rules.
    """
    class Meta:
        model = Trip
        fields = [
            'vehicle',
            'driver',
            'source',
            'destination',
            'cargo_weight',
            'planned_distance',
            'revenue'
        ]
        widgets = {
            'source': forms.TextInput(attrs={'placeholder': 'e.g. Warehouse A, Delhi'}),
            'destination': forms.TextInput(attrs={'placeholder': 'e.g. Client Site B, Mumbai'}),
            'cargo_weight': forms.NumberInput(attrs={'step': '0.01'}),
            'planned_distance': forms.NumberInput(attrs={'step': '0.01'}),
            'revenue': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap styling to form widgets
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs['class'] = classes

        # Dynamic filtering of Vehicles and Drivers status: AVAILABLE
        if self.instance and self.instance.pk:
            # Editing an existing Trip
            self.fields['vehicle'].queryset = Vehicle.objects.filter(
                Q(status=Vehicle.VehicleStatus.AVAILABLE) | Q(pk=self.instance.vehicle.pk)
            )
            self.fields['driver'].queryset = Driver.objects.filter(
                Q(status=Driver.DriverStatus.AVAILABLE) | Q(pk=self.instance.driver.pk)
            )
        else:
            # Creating a new Trip
            self.fields['vehicle'].queryset = Vehicle.objects.filter(status=Vehicle.VehicleStatus.AVAILABLE)
            self.fields['driver'].queryset = Driver.objects.filter(status=Driver.DriverStatus.AVAILABLE)

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        driver = cleaned_data.get('driver')
        cargo_weight = cleaned_data.get('cargo_weight')

        # 1. Cargo Weight must not exceed Vehicle Maximum Load Capacity
        if vehicle and cargo_weight is not None:
            if cargo_weight > vehicle.max_load_capacity:
                self.add_error(
                    'cargo_weight',
                    ValidationError(
                        f"Cargo weight ({cargo_weight} kg) exceeds vehicle max load capacity ({vehicle.max_load_capacity} kg)."
                    )
                )

        # 2. Driver whose license has expired cannot be assigned
        if driver:
            if driver.license_expiry_date < datetime.date.today():
                self.add_error(
                    'driver',
                    ValidationError(
                        f"Driver {driver.full_name} cannot be assigned because their commercial driver license has expired."
                    )
                )

        # 3. Vehicle already On Trip cannot be assigned
        if vehicle:
            # Only raise validation error if the vehicle was newly changed or set
            is_new_vehicle = (self.instance.pk is None) or (self.instance.vehicle != vehicle)
            if is_new_vehicle and vehicle.status == Vehicle.VehicleStatus.ON_TRIP:
                self.add_error(
                    'vehicle',
                    ValidationError("This vehicle is currently on another trip.")
                )

        # 4. Driver already On Trip cannot be assigned
        if driver:
            is_new_driver = (self.instance.pk is None) or (self.instance.driver != driver)
            if is_new_driver and driver.status == Driver.DriverStatus.ON_TRIP:
                self.add_error(
                    'driver',
                    ValidationError("This driver is currently on another trip.")
                )

        return cleaned_data
