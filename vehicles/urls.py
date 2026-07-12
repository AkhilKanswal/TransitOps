from django.urls import path
from . import views

# Application namespace
app_name = 'vehicles'

urlpatterns = [
    # List of all vehicles (homepage of vehicles app)
    path('', views.VehicleListView.as_view(), name='list'),
    
    # Add a new vehicle
    path('add/', views.VehicleCreateView.as_view(), name='create'),
    
    # View details of a specific vehicle
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='detail'),
    
    # Edit an existing vehicle
    path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='update'),
    
    # Delete a vehicle
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='delete'),
]
