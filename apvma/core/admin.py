from django.contrib import admin
from apvma.core.models import Resident, Apartment, Employee, InternalRegiment

admin.site.register(Apartment)
admin.site.register(Resident)
admin.site.register(Employee)
admin.site.register(InternalRegiment)

admin.site.site_header = 'APVMA'
admin.site.index_title = 'APVMA'
admin.site.site_title = 'administração'