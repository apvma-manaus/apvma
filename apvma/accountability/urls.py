from django.urls import path, re_path

from apvma.accountability.views import accountability

urlpatterns = [
    path('', accountability, name='accountability'),
    ]