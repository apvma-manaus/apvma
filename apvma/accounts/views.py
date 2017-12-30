from django.conf import settings
from django.core import mail
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string

from apvma.accounts.forms import RequestSignUpForm


def request_signup(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)

def empty_form(request):
    form = RequestSignUpForm()
    return render(request, 'request_signup_form.html', {'form': form})

def create(request):
    form = RequestSignUpForm(request.POST)

    if not form.is_valid():
        return render(request, 'request_signup_form.html', {'form': form})

    request_signup = form.save()

    # Send email
    _send_mail('Solicitação de cadastro de novo morador',
               request_signup.email,
               settings.DEFAULT_APVMA_EMAIL,
               'request_signup_email.txt',
               {'request_signup': request_signup})

    return render_to_response('request_signup_done.html', {'form': form})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to])