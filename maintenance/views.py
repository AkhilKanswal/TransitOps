from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for maintenance
def maintenance_home(request):
    """
    Placeholder view for the TransitOps Maintenance homepage.
    """
    return HttpResponse("<h1>TransitOps Maintenance</h1><p>Welcome to the Maintenance module.</p>")
