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
    file = os.path.join(settings.MEDIA_ROOT, file)
    pdf = open(file, 'rb').read()
    return HttpResponse(pdf, content_type='application/pdf')
