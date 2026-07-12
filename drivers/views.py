from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for drivers
def drivers_home(request):
    """
    Placeholder view for the TransitOps Drivers homepage.
    """
    return HttpResponse("<h1>TransitOps Drivers</h1><p>Welcome to the Drivers module.</p>")
