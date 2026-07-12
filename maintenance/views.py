from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from vehicles.models import Vehicle
from .models import Maintenance
from .forms import MaintenanceForm


class MaintenanceListView(ListView):
    """
    Lists maintenance records with search, filtering, and pagination.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 10
    ordering = ['-start_date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle')

        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(issue__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(vehicle__registration_number__icontains=search_query)
            )

        vehicle_id = self.request.GET.get('vehicle', '').strip()
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)

        is_active = self.request.GET.get('is_active', '').strip()
        if is_active == 'true':
            queryset = queryset.filter(is_active=True)
        elif is_active == 'false':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all().order_by('registration_number')
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_vehicle'] = self.request.GET.get('vehicle', '').strip()
        context['selected_is_active'] = self.request.GET.get('is_active', '').strip()
        return context


class MaintenanceDetailView(DetailView):
    """
    Displays detailed information for a specific maintenance record.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_detail.html'
    context_object_name = 'maintenance'


class MaintenanceCreateView(SuccessMessageMixin, CreateView):
    """
    Allows fleet managers to log new maintenance work for a vehicle.
    """
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance:list')
    success_message = "Maintenance record for %(vehicle)s was created successfully."

    def form_valid(self, form):
        vehicle = form.cleaned_data['vehicle']
        is_active = form.cleaned_data['is_active']

        if is_active:
            if vehicle.status == Vehicle.VehicleStatus.ON_TRIP:
                form.add_error('vehicle', "Cannot schedule maintenance for a vehicle that is currently on a trip.")
                return self.form_invalid(form)
            if vehicle.status == Vehicle.VehicleStatus.RETIRED:
                form.add_error('vehicle', "Cannot schedule maintenance for a retired vehicle.")
                return self.form_invalid(form)

        with transaction.atomic():
            response = super().form_valid(form)
            if is_active and vehicle.status != Vehicle.VehicleStatus.IN_SHOP:
                vehicle.status = Vehicle.VehicleStatus.IN_SHOP
                vehicle.save(update_fields=['status', 'updated_at'])
        return response


class MaintenanceUpdateView(SuccessMessageMixin, UpdateView):
    """
    Allows editing of existing maintenance records.
    """
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/maintenance_form.html'

    def get_success_url(self):
        return reverse_lazy('maintenance:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return f"Maintenance record for {self.object.vehicle.registration_number} was updated successfully."

    def form_valid(self, form):
        vehicle = form.cleaned_data['vehicle']
        is_active = form.cleaned_data['is_active']

        if is_active:
            if vehicle.status == Vehicle.VehicleStatus.ON_TRIP:
                form.add_error('vehicle', "Cannot mark maintenance as active for a vehicle that is currently on a trip.")
                return self.form_invalid(form)
            if vehicle.status == Vehicle.VehicleStatus.RETIRED:
                form.add_error('vehicle', "Cannot schedule maintenance for a retired vehicle.")
                return self.form_invalid(form)

        with transaction.atomic():
            response = super().form_valid(form)
            if is_active:
                if vehicle.status != Vehicle.VehicleStatus.IN_SHOP:
                    vehicle.status = Vehicle.VehicleStatus.IN_SHOP
                    vehicle.save(update_fields=['status', 'updated_at'])
            elif vehicle.status == Vehicle.VehicleStatus.IN_SHOP:
                vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                vehicle.save(update_fields=['status', 'updated_at'])
        return response


class MaintenanceDeleteView(DeleteView):
    """
    Allows deletion of a maintenance record.
    """
    model = Maintenance
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance:list')

    def delete(self, request, *args, **kwargs):
        maintenance = self.get_object()
        vehicle = maintenance.vehicle

        with transaction.atomic():
            if maintenance.is_active and vehicle.status == Vehicle.VehicleStatus.IN_SHOP:
                vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                vehicle.save(update_fields=['status', 'updated_at'])
            messages.success(
                request,
                f"Maintenance record for {vehicle.registration_number} was deleted successfully."
            )
            return super().delete(request, *args, **kwargs)


class MaintenanceCompleteView(View):
    """
    Marks an active maintenance record as completed and restores vehicle availability.
    """
    def post(self, request, pk):
        maintenance = get_object_or_404(Maintenance, pk=pk)
        vehicle = maintenance.vehicle

        if not maintenance.is_active:
            messages.error(request, "This maintenance record is already completed.")
            return redirect('maintenance:detail', pk=pk)

        try:
            with transaction.atomic():
                maintenance.is_active = False
                maintenance.end_date = timezone.now().date()
                maintenance.save()

                if vehicle.status == Vehicle.VehicleStatus.IN_SHOP:
                    vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                    vehicle.save(update_fields=['status', 'updated_at'])

                messages.success(
                    request,
                    f"Maintenance for {vehicle.registration_number} has been marked as completed."
                )
        except Exception as error:
            messages.error(request, str(error))

        return redirect('maintenance:detail', pk=pk)
