from calendar import Calendar
from datetime import datetime, timedelta, date

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from apvma.reservations.forms import ReservationForm
from apvma.reservations.models import Reservation
from apvma.reservations.serializer import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@login_required
def reservations(request):
    selected_date = date.today()
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if not form.is_valid():
            return render(request, 'reservations/reservations.html')

        reservation = form.save()

        return HttpResponseRedirect(r('reservations'))

    else:
        return reservation_calendar(request, selected_date.year, selected_date.month)


@login_required
def reservation_calendar(request, year, month):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if not form.is_valid():
            return render(request, 'reservations/reservations.html')

        reservation = form.save()

        return HttpResponseRedirect(r('reservation_calendar', year, month))


    else:

        try:
            selected_date = date(int(year), int(month), 1)
        except ValueError:
            raise Http404

        my_reservations = Reservation.objects.filter(user=request.user.pk, date__gte=datetime.now().date())
        reservations = Reservation.objects.all()

        context = {
            'my_reservations': my_reservations,
            'reservations': reservations,
            'selected_date': selected_date,
            'calendar': tuple(_calendar(selected_date)),
            'next': selected_date + timedelta(days=31),
            'previous': selected_date - timedelta(days=1)
        }

        return render(request, 'reservations/reservations.html', context)


def _calendar(selected_date):
    year, month = selected_date.year, selected_date.month

    # Tapiri valid reservations (not cancelled nor expired)
    tp_filters = {'spot': 'TP', 'date__year':  year, 'date__month': month}
    tp_reservations = {b.date: b for b in Reservation.valid_reservations.filter(**tp_filters)}

    # Salão de Festas valid reservations (not cancelled nor expired)
    sf_reservations = Reservation.objects.filter(
        spot='SF', date__year=year, date__month=month,
    )

    sf_filters = {'spot': 'SF', 'date__year':  year, 'date__month': month}
    sf_reservations = {b.date: b for b in Reservation.valid_reservations.filter(**sf_filters)}

    calendar = Calendar(firstweekday=6)
    for week in calendar.monthdatescalendar(year, month):
        yield [(day, tp_reservations.get(day), sf_reservations.get(day)) for day in week]


def check_expiration(reservation):
    created_on = datetime(
        reservation.created_on.year, reservation.created_on.month, reservation.created_on.day,
        reservation.created_on.hour, reservation.created_on.minute
    )
    days_valid = 2
    if (datetime.now() > created_on + timedelta(days=days_valid)) and reservation.paid == False:
        reservation.expired = True
        reservation.save()