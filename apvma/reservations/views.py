from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apvma.reservations.models import Reservation


@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user.pk, date__gte=datetime.now().date())
    context = {'reservations': reservations}
    return render(request, 'reservations/reservations.html', context)

def check_expiration(reservation):
    created_on = datetime(
        reservation.created_on.year, reservation.created_on.month, reservation.created_on.day,
        reservation.created_on.hour, reservation.created_on.minute
    )
    days_valid = 2
    if (datetime.now() > created_on + timedelta(days=days_valid)) and reservation.paid == False:
        reservation.expired = True
        reservation.save()