from calendar import Calendar
from datetime import datetime, timedelta, date

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.viewsets import ModelViewSet

from apvma.core.user_passes_tests import in_resident_group
from apvma.reservations.forms import ReservationForm
from apvma.reservations.models import Reservation, TermsOfUse
from apvma.reservations.serializer import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def request_reservation(request):
    form = ReservationForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request.path)

    user = request.user
    date = form.cleaned_data['date']
    spot = form.cleaned_data['spot']

    check_reservation = Reservation.valid_reservations.filter(
        date=date, spot=spot
    )

    month = date.month
    second_reservation_same_month = Reservation.valid_reservations.filter(user=user, date__month=month, spot=spot)

    if check_reservation:
        messages.warning(request, 'Já existe uma reserva para o local e data selecionados.')
    elif second_reservation_same_month:
        messages.warning(request, 'As regras de uso só permitem 1 reserva de cada ambiente por mês por permissionário.')
    else:
        reservation = form.save()
        messages.info(request,
                      'Reserva agendada com sucesso. Caso o pagamento não seja realizado em até 24 horas, a reserva será expirada.')


def cancel_reservation(request):
    reservation = Reservation.objects.get(pk=request.POST['cancel_reservation'])
    reservation.cancel()

    messages.success(request, 'Reserva cancelada com sucesso.')


@login_required
@user_passes_test(in_resident_group, login_url='/home/')
def reservation_calendar(request, year, month):
    if request.method == 'POST':
        if 'request_reservation_button' in request.POST:
            request_reservation(request)

        if 'cancel_reservation_button' in request.POST:
            cancel_reservation(request)

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
        terms_of_use = TermsOfUse.objects.last()

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
            'maximum_reservation_date': maximum_reservation_date,
            'terms_of_use': terms_of_use
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

    # Tapiri das Arvores valid reservations (not cancelled nor expired)
    ta_reservations = Reservation.objects.filter(
        spot='TA', date__year=year, date__month=month,
    )
    ta_filters = {'spot': 'TA', 'date__year': year, 'date__month': month}
    ta_reservations = {b.date: b for b in Reservation.valid_reservations.filter(**ta_filters)}

    calendar = Calendar(firstweekday=6)
    today = date.today()
    for week in calendar.monthdatescalendar(year, month):
        yield [(day, tp_reservations.get(day), sf_reservations.get(day), ta_reservations.get(day)) for day in week]

