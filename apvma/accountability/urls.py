from django.urls import path

from apvma.accountability.views import accountability

urlpatterns = [
    path('', accountability, name='accountability'),
    ]