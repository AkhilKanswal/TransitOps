import datetime
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.db.models import Q

from vehicles.models import Vehicle
from .models import Maintenance
from .forms import MaintenanceForm

class MaintenanceListView(LoginRequiredMixin, ListView):
    """
    Lists maintenance records with searching, filtering, and pagination.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # 1. Search (Vehicle registration, Issue title)
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(vehicle__registration_number__icontains=search_query) |
                Q(issue_title__icontains=search_query)
            )

        # 2. Status Filter
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)

        # 3. Type Filter
        mtype = self.request.GET.get('maintenance_type', '').strip()
        if mtype:
            queryset = queryset.filter(maintenance_type=mtype)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch filter choices
        context['status_choices'] = Maintenance.MaintenanceStatus.choices
        context['type_choices'] = Maintenance.MaintenanceType.choices

        # Preserving filters in the context for pagination
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        context['selected_type'] = self.request.GET.get('maintenance_type', '').strip()
        return context


class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    """
    Displays details for a specific maintenance record.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_detail.html'
    context_object_name = 'maintenance'


class MaintenanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Allows scheduling or recording vehicle maintenance.
    """
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance:list')
    success_message = "Maintenance record was created successfully."

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            maintenance = self.object
            vehicle = maintenance.vehicle

            # Business rule: If In Progress, update vehicle status -> In Shop
            if maintenance.status == Maintenance.MaintenanceStatus.IN_PROGRESS:
                vehicle.status = Vehicle.VehicleStatus.IN_SHOP
                vehicle.save()
                messages.info(self.request, f"Vehicle {vehicle.registration_number} status set to In Shop.")
            
            # Business rule: If Completed, update vehicle status -> Available (if not retired)
            elif maintenance.status == Maintenance.MaintenanceStatus.COMPLETED:
                if vehicle.status != Vehicle.VehicleStatus.RETIRED:
                    vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                    vehicle.save()
                    messages.info(self.request, f"Vehicle {vehicle.registration_number} status set to Available.")

            return response


class MaintenanceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Allows updating maintenance details.
    """
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/maintenance_form.html'

    def get_success_url(self):
        return reverse_lazy('maintenance:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return f"Maintenance record #{self.object.id} was updated successfully."

    def form_valid(self, form):
        old_status = self.get_object().status
        new_status = form.cleaned_data.get('status')
        vehicle = form.cleaned_data.get('vehicle')

        with transaction.atomic():
            response = super().form_valid(form)
            maintenance = self.object

            # Check if status has changed
            if old_status != new_status:
                if new_status == Maintenance.MaintenanceStatus.IN_PROGRESS:
                    vehicle.status = Vehicle.VehicleStatus.IN_SHOP
                    vehicle.save()
                    messages.info(self.request, f"Vehicle status updated to In Shop.")
                elif new_status == Maintenance.MaintenanceStatus.COMPLETED:
                    if vehicle.status != Vehicle.VehicleStatus.RETIRED:
                        vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                        vehicle.save()
                        messages.info(self.request, f"Vehicle status updated to Available.")
            
            return response


class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows deleting maintenance records.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance:list')

    def delete(self, request, *args, **kwargs):
        maintenance = self.get_object()
        messages.success(self.request, f"Maintenance record #{maintenance.id} deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MaintenanceTransitionView(LoginRequiredMixin, View):
    """
    Handles inline status changes (start, close, cancel) inside database transactions.
    """
    def post(self, request, pk, action):
        maintenance = get_object_or_404(Maintenance, pk=pk)
        vehicle = maintenance.vehicle

        try:
            with transaction.atomic():
                if action == 'start':
                    if maintenance.status != Maintenance.MaintenanceStatus.SCHEDULED:
                        raise ValueError("Only Scheduled maintenance can be started.")
                    
                    maintenance.status = Maintenance.MaintenanceStatus.IN_PROGRESS
                    vehicle.status = Vehicle.VehicleStatus.IN_SHOP
                    messages.success(request, f"Maintenance started. Vehicle {vehicle.registration_number} status set to In Shop.")

                elif action == 'complete':
                    if maintenance.status != Maintenance.MaintenanceStatus.IN_PROGRESS:
                        raise ValueError("Only In Progress maintenance can be marked Completed.")

                    maintenance.status = Maintenance.MaintenanceStatus.COMPLETED
                    maintenance.end_date = datetime.date.today()
                    
                    # Return vehicle to Available status unless it has been retired
                    if vehicle.status != Vehicle.VehicleStatus.RETIRED:
                        vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                    messages.success(request, f"Maintenance Completed. Vehicle {vehicle.registration_number} status updated.")

                elif action == 'cancel':
                    if maintenance.status not in [Maintenance.MaintenanceStatus.SCHEDULED, Maintenance.MaintenanceStatus.IN_PROGRESS]:
                        raise ValueError("Only Scheduled or In Progress maintenance can be Cancelled.")

                    maintenance.status = Maintenance.MaintenanceStatus.CANCELLED
                    # Cancelled maintenance should NOT affect vehicle status (rule 6).
                    messages.success(request, f"Maintenance record #{maintenance.id} has been Cancelled.")

                else:
                    raise ValueError("Invalid transition action requested.")

                # Save changes
                maintenance.save()
                vehicle.save()

        except ValueError as error:
            messages.error(request, str(error))

        return redirect('maintenance:detail', pk=pk)
