from django.urls import path, re_path

from apvma.accountability.views import accountability, pdf_view

urlpatterns = [
    path('', accountability, name='accountability'),
    re_path('(?P<file>[\w]+.pdf)', pdf_view, name='pdf_view')
    ]