from django.urls import path

from apvma.assembly.views import assembly

urlpatterns = [
    path('', assembly, name='assembly'),
    ]
