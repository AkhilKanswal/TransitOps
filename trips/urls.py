from django.urls import path
from . import views

# Application namespace
app_name = 'trips'

urlpatterns = [
    # List of all trips (homepage of trips app)
    path('', views.TripListView.as_view(), name='list'),

    # Create/Register a new trip
    path('add/', views.TripCreateView.as_view(), name='create'),

    # View details of a specific trip
    path('<int:pk>/', views.TripDetailView.as_view(), name='detail'),

    # Edit an existing Draft trip
    path('<int:pk>/edit/', views.TripUpdateView.as_view(), name='update'),

    # Delete a Draft trip
    path('<int:pk>/delete/', views.TripDeleteView.as_view(), name='delete'),

    # Handles transitions: dispatch, complete, cancel
    path('<int:pk>/transition/<str:action>/', views.TripTransitionView.as_view(), name='transition'),
]
