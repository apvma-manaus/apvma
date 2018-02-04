from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apvma.core.models import InternalRegiment


@login_required
def home(request):
    internal_regiment = InternalRegiment.objects.last()
    context = {'internal_regiment': internal_regiment}
    return render(request, 'home.html', context)