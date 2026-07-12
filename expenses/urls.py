from django.urls import path
from django.views.generic import RedirectView
from . import views

# Application namespace
app_name = 'expenses'

urlpatterns = [
    # General Expenses CRUD
    path('', RedirectView.as_view(pattern_name='expenses:list', permanent=False), name='home'),
    path('list/', views.ExpenseListView.as_view(), name='list'),
    path('add/', views.ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ExpenseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='delete'),

    # Fuel Logs CRUD
    path('fuel/', views.FuelLogListView.as_view(), name='fuel_list'),
    path('fuel/add/', views.FuelLogCreateView.as_view(), name='fuel_create'),
    path('fuel/<int:pk>/', views.FuelLogDetailView.as_view(), name='fuel_detail'),
    path('fuel/<int:pk>/edit/', views.FuelLogUpdateView.as_view(), name='fuel_update'),
    path('fuel/<int:pk>/delete/', views.FuelLogDeleteView.as_view(), name='fuel_delete'),
]
