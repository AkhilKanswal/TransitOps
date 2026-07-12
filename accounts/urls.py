from django.urls import path
from . import views

# Application namespace
app_name = 'accounts'

urlpatterns = [
    # Placeholder path for accounts homepage
    path('', views.accounts_home, name='home'),
]
