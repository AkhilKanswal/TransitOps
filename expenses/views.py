from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Expense, FuelLog
from .forms import ExpenseForm, FuelLogForm

# ==========================================
# 1. GENERAL EXPENSES CRUD
# ==========================================

class ExpenseListView(LoginRequiredMixin, ListView):
    """
    Renders general expenses with searching, filtering, and pagination.
    """
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10
    ordering = ['-expense_date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle', 'trip')
        
        # Search by Vehicle Registration Number or Remarks
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(vehicle__registration_number__icontains=q) |
                Q(remarks__icontains=q)
            )

        # Filter by Expense Type
        expense_type = self.request.GET.get('expense_type', '').strip()
        if expense_type:
            queryset = queryset.filter(expense_type=expense_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        context['selected_type'] = self.request.GET.get('expense_type', '').strip()
        context['expense_types'] = Expense.ExpenseType.choices
        return context


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    """
    Renders detailed view for a single general expense.
    """
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'


class ExpenseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Allows logging a new general expense.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')
    success_message = "Expense record was created successfully."


class ExpenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Allows modifying an existing general expense record.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'

    def get_success_url(self):
        return reverse_lazy('expenses:detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return "Expense record was updated successfully."


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows deleting a general expense record.
    """
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')

    def delete(self, request, *args, **kwargs):
        expense = self.get_object()
        messages.success(self.request, f"Expense record #{expense.id} was deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# 2. VEHICLE FUEL LOGS CRUD
# ==========================================

class FuelLogListView(LoginRequiredMixin, ListView):
    """
    Renders vehicle fuel logs with searching and pagination.
    """
    model = FuelLog
    template_name = 'expenses/fuel_log_list.html'
    context_object_name = 'fuel_logs'
    paginate_by = 10
    ordering = ['-log_date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle', 'trip')

        # Search by Vehicle Registration Number
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(vehicle__registration_number__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class FuelLogDetailView(LoginRequiredMixin, DetailView):
    """
    Renders detailed view for a single fuel log record.
    """
    model = FuelLog
    template_name = 'expenses/fuel_log_detail.html'
    context_object_name = 'fuel_log'


class FuelLogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Allows registering a new fuel log.
    """
    model = FuelLog
    form_class = FuelLogForm
    template_name = 'expenses/fuel_log_form.html'
    success_url = reverse_lazy('expenses:fuel_list')
    success_message = "Fuel log was created successfully."


class FuelLogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Allows modifying an existing fuel log record.
    """
    model = FuelLog
    form_class = FuelLogForm
    template_name = 'expenses/fuel_log_form.html'

    def get_success_url(self):
        return reverse_lazy('expenses:fuel_detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return "Fuel log was updated successfully."


class FuelLogDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows deleting a fuel log record.
    """
    model = FuelLog
    template_name = 'expenses/fuel_log_confirm_delete.html'
    success_url = reverse_lazy('expenses:fuel_list')

    def delete(self, request, *args, **kwargs):
        fuel_log = self.get_object()
        messages.success(self.request, f"Fuel log #{fuel_log.id} was deleted successfully.")
        return super().delete(request, *args, **kwargs)
