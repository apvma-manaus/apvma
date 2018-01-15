from calendar import Calendar
from datetime import datetime, timedelta, date

from django.contrib import messages
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
        if len(request.POST) == 4: # POST requesting new reservation
            form = ReservationForm(request.POST)

            if not form.is_valid():
                return HttpResponseRedirect(request.path)

            check_reservation = Reservation.valid_reservations.filter(
                date=request.POST['date'], spot=request.POST['spot']
            )

            if check_reservation:
                messages.warning(request, 'Já existe uma reserva para o local e data selecionados.')
            else:
                reservation = form.save()
                messages.success(request,
                                 'Reserva agendada com sucesso. Caso o pagamento não seja realizado até amanhã, a reserva será expirada.')

        if len(request.POST) == 3: # POST requesting cancel reservation
            reservation = Reservation.objects.get(pk=request.POST['cancel_reservation'])
            reservation.cancel()

            messages.success(request, 'Reserva cancelada com sucesso.')

        return HttpResponseRedirect(request.path)


    else:
        return reservation_calendar(request, selected_date.year, selected_date.month)

@login_required
def reservation_calendar(request, year, month):
    if request.method == 'POST':
        if len(request.POST) == 4: # POST requesting new reservation
            form = ReservationForm(request.POST)

            if not form.is_valid():
                return HttpResponseRedirect(request.path)

            check_reservation = Reservation.valid_reservations.filter(
                date=request.POST['date'], spot=request.POST['spot']
            )

            if check_reservation:
                messages.warning(request, 'Já existe uma reserva para o local e data selecionados.')
            else:
                reservation = form.save()
                messages.success(request,
                                 'Reserva agendada com sucesso. Caso o pagamento não seja realizado em até 24 horas, a reserva será expirada.')

        if len(request.POST) == 3: # POST requesting cancel reservation
            reservation = Reservation.objects.get(pk=request.POST['cancel_reservation'])
            reservation.cancel()

            messages.success(request, 'Reserva cancelada com sucesso.')

        return HttpResponseRedirect(request.path)

    else:

        try:
            selected_date = date(int(year), int(month), 1)
        except ValueError:
            raise Http404

        my_reservations = Reservation.objects.filter(user=request.user.pk, date__gte=datetime.now().date())
        my_valid_reservations = Reservation.valid_reservations.filter(user=request.user.pk, date__gte=datetime.now().date())
        reservations = Reservation.valid_reservations.all()
        today = date.today()
        maximum_reservation_date = today + timedelta(days=90)

        context = {
            'my_reservations': my_reservations,
            'my_valid_reservations': my_valid_reservations,
            'reservations': reservations,
            'selected_date': selected_date,
            'calendar': tuple(_calendar(selected_date)),
            'next': selected_date + timedelta(days=31),
            'previous': selected_date - timedelta(days=1),
            'today': today,
            'minimum_reservation_date': today + timedelta(days=1),
            'maximum_reservation_date': maximum_reservation_date
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
    today = date.today()
    for week in calendar.monthdatescalendar(year, month):
        yield [(day, tp_reservations.get(day), sf_reservations.get(day)) for day in week]

