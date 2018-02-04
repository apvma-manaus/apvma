from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apvma.accountability.models import Accountability


@login_required
def accountability(request):
    accountabilities = Accountability.objects.all().order_by('-date')[:12]
    context = {'accountabilities': accountabilities}
    return render(request, 'accountability/accountability.html', context)
