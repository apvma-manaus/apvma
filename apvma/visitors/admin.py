from django.contrib import admin

from apvma.core.models import Apartment, Resident
from apvma.visitors.models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'description', 'apartment', 'resident', 'card', 'arrival_time', 'exit_time']
    list_filter = ['datetime',]
    list_editable = ['card', 'arrival_time', 'exit_time']

    def apartment(self, obj):
        apartment = Apartment.objects.get(user=obj.user)
        return apartment

    def resident(self, obj):
        resident = Resident.objects.get(apartment__user=obj.user)
        return resident

    apartment.short_description = 'apartamento'
    resident.short_description = 'morador'

admin.site.register(Visitor, VisitorAdmin)