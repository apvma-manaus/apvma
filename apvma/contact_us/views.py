from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from apvma.contact_us.forms import ContactUsForm
from apvma.core.models import Resident, Apartment


@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if not form.is_valid():
            return render(request, 'contact_us/contact_us.html', {'form': form})

        import ipdb
        #ipdb.set_trace()
        if form.cleaned_data['identify'] == '1':
            user = request.user
            resident = Resident.objects.get(apartment__user=user)
            email_from = resident.email
            msg = 'Obrigado por entrar em contato conosco e nos ajudar a trazer melhorias para a nossa vila.'
        else:
            user = 'Mensagem anônima'
            resident = 'Mensagem anônima'
            email_from = settings.DEFAULT_APVMA_EMAIL
            msg = 'Obrigado por entrar em contato conosco e nos ajudar a trazer melhorias para a nossa vila. \n' \
                  'Não se preocupe, a mensagem foi enviada como anônima e você não será identificado.'

        # Send email
        _send_mail('Mensagem do "Entre em contato conosco"',
                   email_from,
                   settings.DEFAULT_APVMA_EMAIL,
                   'contact_us/contact_us_email.txt',
                   {'form': form.cleaned_data, 'user': user, 'resident': resident})

        messages.success(request, msg)
        return HttpResponseRedirect(r('contact_us'))

    context = {'form': ContactUsForm()}

    return render(request, 'contact_us/contact_us.html', context)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to,])