from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserProfileForm

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Renders the details of the currently logged-in user.
    """
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        # Always return the currently logged-in user
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Allows the logged-in user to update their first name, last name, and email.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'registration/profile_form.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Your profile was updated successfully."

    def get_object(self, queryset=None):
        # Always return the currently logged-in user
        return self.request.user
