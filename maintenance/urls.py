from django.urls import path
from . import views

# Application namespace
app_name = 'maintenance'

urlpatterns = [
    # Placeholder path for maintenance homepage
    path('', views.maintenance_home, name='home'),
]
