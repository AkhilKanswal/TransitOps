from django.urls import path
from . import views

# Application namespace
app_name = 'expenses'

urlpatterns = [
    # Placeholder path for expenses homepage
    path('', views.expenses_home, name='home'),
]
