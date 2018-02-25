from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from apvma.assembly.models import Assembly
from apvma.core.user_passes_tests import in_resident_group


@login_required
@user_passes_test(in_resident_group, login_url='/home/')
def assembly(request):
    assemblies = Assembly.objects.all().order_by('-date')
    context = {'assemblies': assemblies}
    return render(request, 'assembly/assembly.html', context)
