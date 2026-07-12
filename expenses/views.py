from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for expenses
def expenses_home(request):
    """
    Placeholder view for the TransitOps Expenses homepage.
    """
    return HttpResponse("<h1>TransitOps Expenses</h1><p>Welcome to the Expenses module.</p>")
