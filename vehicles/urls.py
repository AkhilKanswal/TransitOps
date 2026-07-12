from django.urls import path
from . import views

# Application namespace
app_name = 'vehicles'

urlpatterns = [
    # Placeholder path for vehicles homepage
    path('', views.vehicles_home, name='home'),
]
