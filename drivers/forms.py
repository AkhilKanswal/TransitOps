import datetime
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Driver

class DriverForm(forms.ModelForm):
    """
    ModelForm for adding and editing Fleet Drivers in TransitOps.
    Includes custom validations for license expiry, safety score, and contact info.
    """
    class Meta:
        model = Driver
        fields = [
            'full_name',
            'license_number',
            'license_category',
            'license_expiry_date',
            'contact_number',
            'safety_score',
            'status'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g. Rajesh Kumar'}),
            'license_number': forms.TextInput(attrs={'placeholder': 'e.g. DL-1234567890123'}),
            'license_category': forms.TextInput(attrs={'placeholder': 'e.g. Heavy Motor Vehicle'}),
            'license_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'e.g. +91 98765 43210'}),
            'safety_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'status': forms.Select(),
        }

    def __init__(self, *source, **options):
        super().__init__(*source, **options)
        # Apply Bootstrap styling to form widgets
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs['class'] = classes

    def clean_license_expiry_date(self):
        expiry_date = self.cleaned_data.get('license_expiry_date')
        if expiry_date:
            # Only validate expiry date in the future when creating a new record
            if self.instance.pk is None and expiry_date < datetime.date.today():
                raise ValidationError("License expiry date cannot be in the past when registering a new driver.")
        return expiry_date

    def clean_safety_score(self):
        score = self.cleaned_data.get('safety_score')
        if score is not None:
            if score < 0 or score > 100:
                raise ValidationError("Safety score must be between 0 and 100.")
        return score

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number', '').strip()
        if contact:
            # Match standard digits, spaces, hyphens, and + at the beginning, length 7 to 15 digits
            pattern = re.compile(r'^\+?[0-9\s\-]{7,15}$')
            if not pattern.match(contact):
                raise ValidationError("Please enter a valid contact number (7 to 15 digits, optionally starting with +).")
        return contact
