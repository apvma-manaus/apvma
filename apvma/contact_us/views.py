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

        user = request.user
        resident = Resident.objects.get(apartment__user=user)
        email_to = resident.email

        # Send email
        _send_mail('Mensagem do "Entre em contato conosco"',
                   email_to,
                   settings.DEFAULT_APVMA_EMAIL,
                   'contact_us/contact_us_email.txt',
                   {'form': form.cleaned_data, 'user': user, 'resident': resident})

        messages.success(request, 'Obrigado por entrar em contato conosco e nos ajudar a trazer melhorias para a nossa vila.')
        return HttpResponseRedirect(r('contact_us'))

    context = {'form': ContactUsForm()}

    return render(request, 'contact_us/contact_us.html', context)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to,])