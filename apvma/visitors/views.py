from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from apvma.core.models import Apartment
from apvma.core.user_passes_tests import in_resident_group
from apvma.visitors.forms import AuthorizeVisitorForm
from apvma.visitors.models import Visitor


@login_required
@user_passes_test(in_resident_group, login_url='/home/')
def visitors(request):
    if request.method == 'POST':
        if 'new_authorization_button' in request.POST:
            new_authorization(request)

        if 'cancel_authorization_button' in request.POST:
            cancel_authorization(request)

        return HttpResponseRedirect(request.path)

    else:
        form = AuthorizeVisitorForm()
        my_visitors_planned = Visitor.objects.filter(
            apartment__user=request.user).filter(Q(exit_time=None) |
                                         Q(datetime__gte=datetime.today())).order_by('datetime')
        context = {'my_visitors_planned': my_visitors_planned,
                   'form': form}
        return render(request, 'visitors/visitors.html', context)

def new_authorization(request):
    _datetime = datetime.strptime(request.POST['datetime'], '%d/%m/%y - %H:%M')
    description = request.POST['description']
    apartment = Apartment.objects.get(user=request.user)
    Visitor.objects.create(datetime=_datetime,
                           description=description,
                           apartment=apartment)

    messages.success(request, 'Autorização enviada com sucesso.')


def cancel_authorization(request):
    """Delete a visitor object selected by user"""
    visit = Visitor.objects.get(pk=request.POST['cancel_authorization'])
    visit.delete()

    messages.success(request, 'Autorização cancelada com sucesso.')