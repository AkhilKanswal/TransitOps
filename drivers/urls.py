from django.urls import path
from . import views

# Application namespace
app_name = 'drivers'

urlpatterns = [
    # Placeholder path for drivers homepage
    path('', views.drivers_home, name='home'),
]
