from django import forms
from django.core.exceptions import ValidationError
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    """
    ModelForm for adding and editing Fleet Vehicles in TransitOps.
    Includes custom validation for odometer, load capacity, and cost.
    """
    class Meta:
        model = Vehicle
        fields = [
            'registration_number',
            'model_name',
            'vehicle_type',
            'max_load_capacity',
            'current_odometer',
            'acquisition_cost',
            'status'
        ]
        widgets = {
            'registration_number': forms.TextInput(attrs={'placeholder': 'e.g. DL 1CA 1234'}),
            'model_name': forms.TextInput(attrs={'placeholder': 'e.g. Tata Prima 4025.S'}),
            'vehicle_type': forms.TextInput(attrs={'placeholder': 'e.g. Heavy Duty Truck'}),
            'max_load_capacity': forms.NumberInput(attrs={'step': '0.01'}),
            'current_odometer': forms.NumberInput(attrs={'min': '0'}),
            'acquisition_cost': forms.NumberInput(attrs={'step': '0.01'}),
            'status': forms.Select(),
        }

    def __init__(self, *source, **options):
        super().__init__(*source, **options)
        # Apply Bootstrap styling to each form widget
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs['class'] = classes

    def clean_max_load_capacity(self):
        capacity = self.cleaned_data.get('max_load_capacity')
        if capacity is not None and capacity <= 0:
            raise ValidationError("Maximum load capacity must be greater than 0.")
        return capacity

    def clean_current_odometer(self):
        odometer = self.cleaned_data.get('current_odometer')
        if odometer is not None and odometer < 0:
            raise ValidationError("Current odometer reading cannot be negative.")
        return odometer

    def clean_acquisition_cost(self):
        cost = self.cleaned_data.get('acquisition_cost')
        if cost is not None and cost < 0:
            raise ValidationError("Acquisition cost cannot be negative.")
        return cost
