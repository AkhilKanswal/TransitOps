from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for vehicles
def vehicles_home(request):
    """
    Placeholder view for the TransitOps Vehicles homepage.
    """
    return HttpResponse("<h1>TransitOps Vehicles</h1><p>Welcome to the Vehicles module.</p>")
