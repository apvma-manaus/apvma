"""apvma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from rest_framework import routers

from apvma.core.views import home
from apvma.accounts import views as account_views
from apvma.reservations.views import ReservationViewSet

router = routers.DefaultRouter()
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='index'),

    # login urls
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('request_signup/', account_views.request_signup, name='request_signup'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),

    # password reset urls
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    # password change urls
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

    # accountability urls
    path('accountability/', include('apvma.accountability.urls')),

    # reservations urls
    path('reservations/', include('apvma.reservations.urls')),

    # reservation calendar api
    path('api/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),

    # contact_us urls
    path('contact_us', include('apvma.contact_us.urls'))
]
