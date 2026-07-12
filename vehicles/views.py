from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

class VehicleListView(LoginRequiredMixin, ListView):
    """
    Renders the list of fleet vehicles with support for searching,
    filtering, sorting, and pagination (10 per page).
    """
    model = Vehicle
    template_name = 'vehicles/list.html'
    context_object_name = 'vehicles'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(registration_number__icontains=search_query) |
                Q(model_name__icontains=search_query)
            )

        # Vehicle Type filter
        vehicle_type = self.request.GET.get('vehicle_type', '').strip()
        if vehicle_type:
            queryset = queryset.filter(vehicle_type__iexact=vehicle_type)

        # Status filter
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch unique vehicle types dynamically from database for the filter dropdown
        context['vehicle_types'] = Vehicle.objects.values_list('vehicle_type', flat=True).distinct().order_by('vehicle_type')
        # Fetch status choices from the model
        context['status_choices'] = Vehicle.VehicleStatus.choices
        # Preserve active filters in context for pagination links
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_type'] = self.request.GET.get('vehicle_type', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        return context


class VehicleDetailView(LoginRequiredMixin, DetailView):
    """
    Renders detailed information for a specific vehicle.
    """
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'


class VehicleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Allows fleet managers to add new vehicles.
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')
    success_message = "Vehicle %(registration_number)s was added successfully."


class VehicleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Allows fleet managers to modify existing vehicle records.
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    
    def get_success_url(self):
        # Redirect to the vehicle detail view on successful update
        return reverse_lazy('vehicles:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return f"Vehicle {self.object.registration_number} was updated successfully."


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows deletion of a vehicle record. Handles success message safely.
    """
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicles:list')

    def delete(self, request, *args, **kwargs):
        vehicle = self.get_object()
        messages.success(self.request, f"Vehicle {vehicle.registration_number} was deleted successfully.")
        return super().delete(request, *args, **kwargs)
