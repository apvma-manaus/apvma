from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apvma.reservations.models import Reservation


@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user.pk, date__gt=datetime.now().date())
    context = {'reservations': reservations}
    return render(request, 'reservations/reservations.html', context)