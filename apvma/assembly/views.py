from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apvma.assembly.models import Assembly


@login_required
def assembly(request):
    assemblies = Assembly.objects.all().order_by('-date')
    context = {'assemblies': assemblies}
    return render(request, 'assembly/assembly.html', context)
