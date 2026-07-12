from django.urls import path
from . import views

# Application namespace
app_name = 'maintenance'

urlpatterns = [
    # List of all maintenance records
    path('', views.MaintenanceListView.as_view(), name='list'),

    # Create a new maintenance record
    path('add/', views.MaintenanceCreateView.as_view(), name='create'),

    # View details of a specific maintenance record
    path('<int:pk>/', views.MaintenanceDetailView.as_view(), name='detail'),

    # Edit an existing maintenance record
    path('<int:pk>/edit/', views.MaintenanceUpdateView.as_view(), name='update'),

    # Delete a maintenance record
    path('<int:pk>/delete/', views.MaintenanceDeleteView.as_view(), name='delete'),

    # Handles transitions: start, complete, cancel
    path('<int:pk>/transition/<str:action>/', views.MaintenanceTransitionView.as_view(), name='transition'),
]
