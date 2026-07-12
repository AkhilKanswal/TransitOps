from django.shortcuts import render
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip

def dashboard_home(request):
    """
    Renders the operational dashboard with real fleet statistics.
    """
    total_drivers = Driver.objects.count()
    active_vehicles = Vehicle.objects.filter(
        status__in=[Vehicle.VehicleStatus.AVAILABLE, Vehicle.VehicleStatus.ON_TRIP]
    ).count()
    ongoing_trips = Trip.objects.filter(status=Trip.TripStatus.DISPATCHED).count()
    total_alerts = Vehicle.objects.filter(
        status__in=[Vehicle.VehicleStatus.IN_SHOP, Vehicle.VehicleStatus.RETIRED]
    ).count()
    recent_trips = Trip.objects.all().order_by('-created_at')[:5]

    context = {
        'total_drivers': total_drivers,
        'active_vehicles': active_vehicles,
        'ongoing_trips': ongoing_trips,
        'total_alerts': total_alerts,
        'recent_trips': recent_trips,
    }
    return render(request, 'dashboard/dashboard.html', context)
