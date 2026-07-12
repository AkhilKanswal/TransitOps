from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for dashboard
def dashboard_home(request):
    """
    Placeholder view for the TransitOps Dashboard homepage.
    """
    return HttpResponse("<h1>TransitOps Dashboard</h1><p>Welcome to the Dashboard module.</p>")
