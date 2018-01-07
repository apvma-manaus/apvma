import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apvma.accountability.models import Accountability


@login_required
def accountability(request):
    accountabilities = Accountability.objects.all().order_by('-date')[:12]
    context = {'accountabilities': accountabilities}
    return render(request, 'accountability/accountability.html', context)

@login_required
def pdf_view(request, file):
    fpath = os.path.join(settings.MEDIA_ROOT, file)
    with open(fpath, 'rb') as pdf:
        return HttpResponse(pdf.read(), content_type='application/pdf')
