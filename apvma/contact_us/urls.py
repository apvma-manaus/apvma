from django.urls import path

from apvma.contact_us.views import contact_us

urlpatterns = [
    path('', contact_us, name='contact_us'),
    ]
