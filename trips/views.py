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
from drivers.models import Driver
from .models import Trip
from .forms import TripForm

class TripListView(ListView):
    """
    Lists operational trips with searching, filtering, and pagination.
    """
    model = Trip
    template_name = 'trips/list.html'
    context_object_name = 'trips'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # 1. Search Query (Trip ID, Vehicle registration, Driver name, Source, Destination)
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            query_filter = Q(source__icontains=search_query) | \
                           Q(destination__icontains=search_query) | \
                           Q(vehicle__registration_number__icontains=search_query) | \
                           Q(driver__full_name__icontains=search_query)
            # If the search query is numeric, check if it matches the Trip ID
            if search_query.isdigit():
                query_filter |= Q(id=int(search_query))
            
            queryset = queryset.filter(query_filter)

        # 2. Status Filter
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)

        # 3. Vehicle Filter
        vehicle_id = self.request.GET.get('vehicle', '').strip()
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)

        # 4. Driver Filter
        driver_id = self.request.GET.get('driver', '').strip()
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch status choices from the model
        context['status_choices'] = Trip.TripStatus.choices
        # Fetch all vehicles and drivers for the filter dropdowns
        context['vehicles'] = Vehicle.objects.all().order_by('registration_number')
        context['drivers'] = Driver.objects.all().order_by('full_name')
        
        # Preserving filters in the context for pagination
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        context['selected_vehicle'] = self.request.GET.get('vehicle', '').strip()
        context['selected_driver'] = self.request.GET.get('driver', '').strip()
        return context


class TripDetailView(DetailView):
    """
    Displays detail information for a specific operational trip.
    """
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'


class TripCreateView(SuccessMessageMixin, CreateView):
    """
    Allows managers to register/create new trips in DRAFT status.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trips:list')
    success_message = "Trip created successfully as a Draft."

    def form_valid(self, form):
        # Explicitly ensure status is set to Draft on create
        form.instance.status = Trip.TripStatus.DRAFT
        return super().form_valid(form)


class TripUpdateView(SuccessMessageMixin, UpdateView):
    """
    Allows editing of Trips. ONLY trips in DRAFT status can be modified.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'

    def dispatch(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.status != Trip.TripStatus.DRAFT:
            messages.error(request, "Access denied. Only Draft trips can be modified.")
            return redirect('trips:detail', pk=trip.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('trips:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return f"Trip #{self.object.id} was updated successfully."


class TripDeleteView(DeleteView):
    """
    Allows deletion of Trips. ONLY trips in DRAFT status can be deleted.
    """
    model = Trip
    template_name = 'trips/trip_confirm_delete.html'
    success_url = reverse_lazy('trips:list')

    def dispatch(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.status != Trip.TripStatus.DRAFT:
            messages.error(request, "Access denied. Only Draft trips can be deleted.")
            return redirect('trips:detail', pk=trip.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        trip = self.get_object()
        messages.success(self.request, f"Trip #{trip.id} was deleted successfully.")
        return super().delete(request, *args, **kwargs)


class TripTransitionView(View):
    """
    Handles lifecycle state changes (dispatch, complete, cancel) for Trips inside database transactions.
    """
    def post(self, request, pk, action):
        trip = get_object_or_404(Trip, pk=pk)
        vehicle = trip.vehicle
        driver = trip.driver

        try:
            with transaction.atomic():
                if action == 'dispatch':
                    # Validate transition preconditions
                    if trip.status != Trip.TripStatus.DRAFT:
                        raise ValueError("Only Draft trips can be Dispatched.")
                    if vehicle.status == Vehicle.VehicleStatus.ON_TRIP:
                        raise ValueError("Vehicle is already assigned to an active trip.")
                    if driver.status == Driver.DriverStatus.ON_TRIP:
                        raise ValueError("Driver is already assigned to an active trip.")
                    if driver.license_expiry_date < timezone.now().date():
                        raise ValueError("Driver's commercial license has expired.")

                    # Transition states
                    trip.status = Trip.TripStatus.DISPATCHED
                    trip.start_date = timezone.now()
                    vehicle.status = Vehicle.VehicleStatus.ON_TRIP
                    driver.status = Driver.DriverStatus.ON_TRIP
                    messages.success(request, f"Trip #{trip.id} has been Dispatched.")

                elif action == 'complete':
                    if trip.status != Trip.TripStatus.DISPATCHED:
                        raise ValueError("Only Dispatched trips can be Completed.")

                    trip.status = Trip.TripStatus.COMPLETED
                    trip.end_date = timezone.now()
                    vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                    driver.status = Driver.DriverStatus.AVAILABLE
                    messages.success(request, f"Trip #{trip.id} Completed successfully.")

                elif action == 'cancel':
                    if trip.status not in [Trip.TripStatus.DRAFT, Trip.TripStatus.DISPATCHED]:
                        raise ValueError("Only Draft or Dispatched trips can be Cancelled.")

                    trip.status = Trip.TripStatus.CANCELLED
                    vehicle.status = Vehicle.VehicleStatus.AVAILABLE
                    driver.status = Driver.DriverStatus.AVAILABLE
                    messages.success(request, f"Trip #{trip.id} has been Cancelled.")

                else:
                    raise ValueError("Invalid lifecycle action requested.")

                # Save all updated states
                trip.save()
                vehicle.save()
                driver.save()

        except ValueError as error:
            messages.error(request, str(error))

        return redirect('trips:detail', pk=pk)
