from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    """
    Form for updating current user profile details (first name, last name, email).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email address is required.")
        return email
