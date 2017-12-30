from django.conf import settings
from django.contrib.auth import login
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.shortcuts import resolve_url as r
from django.template.loader import render_to_string

from apvma.accounts.forms import SignUpForm, RequestSignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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