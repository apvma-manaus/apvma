from django.urls import path, re_path

from apvma.reservations.views import reservations, reservation_calendar

urlpatterns = [
    path('', reservations, name='reservations'),
    re_path(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/$', reservation_calendar, name='reservation_calendar'),
    ]