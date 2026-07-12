from django import forms
from .models import Expense, FuelLog

class ExpenseForm(forms.ModelForm):
    """
    Form for creating and editing general expenses.
    """
    class Meta:
        model = Expense
        fields = ['vehicle', 'trip', 'expense_type', 'amount', 'expense_date', 'remarks']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-light'}),
            'vehicle': forms.Select(attrs={'class': 'form-select bg-light'}),
            'trip': forms.Select(attrs={'class': 'form-select bg-light'}),
            'expense_type': forms.Select(attrs={'class': 'form-select bg-light'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control bg-light', 'step': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control bg-light', 'rows': 4}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Expense amount must be greater than zero.")
        return amount


class FuelLogForm(forms.ModelForm):
    """
    Form for creating and editing vehicle fuel logs.
    """
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'trip', 'fuel_liters', 'fuel_cost', 'log_date']
        widgets = {
            'log_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-light'}),
            'vehicle': forms.Select(attrs={'class': 'form-select bg-light'}),
            'trip': forms.Select(attrs={'class': 'form-select bg-light'}),
            'fuel_liters': forms.NumberInput(attrs={'class': 'form-control bg-light', 'step': '0.01'}),
            'fuel_cost': forms.NumberInput(attrs={'class': 'form-control bg-light', 'step': '0.01'}),
        }

    def clean_fuel_liters(self):
        liters = self.cleaned_data.get('fuel_liters')
        if liters is not None and liters <= 0:
            raise forms.ValidationError("Fuel volume (liters) must be greater than zero.")
        return liters

    def clean_fuel_cost(self):
        cost = self.cleaned_data.get('fuel_cost')
        if cost is not None and cost <= 0:
            raise forms.ValidationError("Fuel cost must be greater than zero.")
        return cost
