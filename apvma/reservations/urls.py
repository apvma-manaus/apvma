from django.urls import path

from apvma.reservations.views import reservations

urlpatterns = [
    path('', reservations, name='reservations'),
    ]