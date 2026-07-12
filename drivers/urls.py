from django.urls import path
from . import views

# Application namespace
app_name = 'drivers'

urlpatterns = [
    # List of all drivers (homepage of drivers app)
    path('', views.DriverListView.as_view(), name='list'),

    # Add/Register a new driver
    path('add/', views.DriverCreateView.as_view(), name='create'),

    # View details of a specific driver
    path('<int:pk>/', views.DriverDetailView.as_view(), name='detail'),

    # Edit an existing driver profile
    path('<int:pk>/edit/', views.DriverUpdateView.as_view(), name='update'),

    # Delete a driver
    path('<int:pk>/delete/', views.DriverDeleteView.as_view(), name='delete'),
]
