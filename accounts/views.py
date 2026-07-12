from django.http import HttpResponse
from django.shortcuts import render

# Placeholder view for accounts
def accounts_home(request):
    """
    Placeholder view for the TransitOps Accounts homepage.
    """
    return HttpResponse("<h1>TransitOps Accounts</h1><p>Welcome to the Accounts module.</p>")
