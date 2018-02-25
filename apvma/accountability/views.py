from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from apvma.accountability.models import Accountability
from apvma.core.user_passes_tests import in_resident_group


@login_required
@user_passes_test(in_resident_group, login_url='/home/')
def accountability(request):
    accountabilities = Accountability.objects.all().order_by('-date')[:12]
    context = {'accountabilities': accountabilities}
    return render(request, 'accountability/accountability.html', context)
