from django import forms
from django.core.exceptions import ValidationError
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    """
    ModelForm for adding and editing vehicle maintenance records in TransitOps.
    """
    class Meta:
        model = Maintenance
        fields = [
            'vehicle',
            'issue',
            'description',
            'maintenance_cost',
            'start_date',
            'end_date',
            'is_active',
        ]
        widgets = {
            'vehicle': forms.Select(),
            'issue': forms.TextInput(attrs={'placeholder': 'e.g. Engine Tune-up, Oil Change'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the maintenance work in detail...'}),
            'maintenance_cost': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_active': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_maintenance_cost(self):
        cost = self.cleaned_data.get('maintenance_cost')
        if cost is not None and cost < 0:
            raise ValidationError("Maintenance cost cannot be negative.")
        return cost

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_active = cleaned_data.get('is_active')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be earlier than the start date.")

        if not is_active and not end_date:
            self.add_error('end_date', "End date is required when marking maintenance as completed.")

        if is_active and end_date:
            self.add_error('end_date', "Clear the end date for ongoing maintenance, or mark it as completed.")

        return cleaned_data
