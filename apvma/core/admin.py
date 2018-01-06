from django.contrib import admin
from apvma.core.models import Resident, Apartment, Employee


admin.site.register(Apartment)
admin.site.register(Resident)
admin.site.register(Employee)
