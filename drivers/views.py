from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Driver
from .forms import DriverForm

class DriverListView(ListView):
    """
    Renders the list of drivers with support for searching,
    filtering, sorting, and pagination (10 per page).
    """
    model = Driver
    template_name = 'drivers/driver_list.html'
    context_object_name = 'drivers'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search filter
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(license_number__icontains=search_query)
            )

        # Status filter
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)

        # License Category filter
        license_category = self.request.GET.get('license_category', '').strip()
        if license_category:
            queryset = queryset.filter(license_category__iexact=license_category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch unique license categories dynamically for filter dropdown
        context['license_categories'] = Driver.objects.values_list('license_category', flat=True).distinct().order_by('license_category')
        # Fetch status choices from the model
        context['status_choices'] = Driver.DriverStatus.choices
        # Preserve active filters in context for pagination links
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        context['selected_category'] = self.request.GET.get('license_category', '').strip()
        return context


class DriverDetailView(DetailView):
    """
    Renders detailed information for a specific driver.
    """
    model = Driver
    template_name = 'drivers/driver_detail.html'
    context_object_name = 'driver'


class DriverCreateView(SuccessMessageMixin, CreateView):
    """
    Allows operations managers to add/register new drivers.
    """
    model = Driver
    form_class = DriverForm
    template_name = 'drivers/driver_form.html'
    success_url = reverse_lazy('drivers:list')
    success_message = "Driver %(full_name)s was registered successfully."


class DriverUpdateView(SuccessMessageMixin, UpdateView):
    """
    Allows operations managers to modify existing driver records.
    """
    model = Driver
    form_class = DriverForm
    template_name = 'drivers/driver_form.html'

    def get_success_url(self):
        # Redirect to details page on successful update
        return reverse_lazy('drivers:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return f"Driver {self.object.full_name} was updated successfully."


class DriverDeleteView(DeleteView):
    """
    Allows operations managers to delete a driver record.
    """
    model = Driver
    template_name = 'drivers/driver_confirm_delete.html'
    success_url = reverse_lazy('drivers:list')

    def delete(self, request, *args, **kwargs):
        driver = self.get_object()
        messages.success(self.request, f"Driver {driver.full_name} was deleted successfully.")
        return super().delete(request, *args, **kwargs)
