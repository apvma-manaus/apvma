from django.urls import path

from apvma.visitors.views import visitors

urlpatterns = [
    path('', visitors, name='visitors'),
    ]
