from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.MaintenanceListView.as_view(), name='list'),
    path('add/', views.MaintenanceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MaintenanceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MaintenanceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MaintenanceDeleteView.as_view(), name='delete'),
    path('<int:pk>/complete/', views.MaintenanceCompleteView.as_view(), name='complete'),
]
