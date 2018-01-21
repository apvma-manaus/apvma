from django.urls import re_path

from apvma.reservations.views import reservation_calendar

urlpatterns = [
    re_path(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/$', reservation_calendar, name='reservation_calendar'),
    ]