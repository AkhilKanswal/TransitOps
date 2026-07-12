from django.urls import path
from . import views

# Application namespace
app_name = 'dashboard'

urlpatterns = [
    # Placeholder path for dashboard homepage
    path('', views.dashboard_home, name='home'),
]
