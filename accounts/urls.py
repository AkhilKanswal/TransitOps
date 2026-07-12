from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

# Application namespace
app_name = 'accounts'

urlpatterns = [
    # Profile Detail & Edit
    path('', RedirectView.as_view(pattern_name='accounts:profile', permanent=False), name='home'),
    path('profile/', views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='edit'),

    # Built-in Password Change Views
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url=reverse_lazy('accounts:password_change_done')
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # Built-in Logout View
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='registration/logged_out.html'
        ),
        name='logout'
    ),
]
