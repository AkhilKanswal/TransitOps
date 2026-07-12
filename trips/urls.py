from django.urls import path
from . import views

# Application namespace
app_name = 'trips'

urlpatterns = [
    # Placeholder path for trips homepage
    path('', views.trips_home, name='home'),
]
