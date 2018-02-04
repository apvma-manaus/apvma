from django.contrib import admin
from apvma.core.models import Resident, Apartment, Employee, InternalRegiment, Statute


class InternalRegimentModelAdmin(admin.ModelAdmin):
    list_display = ('uploaded_on', 'file')
    fields = ('file',)


class StatuteModelAdmin(admin.ModelAdmin):
    list_display = ('uploaded_on', 'file')
    fields = ('file',)


admin.site.register(Apartment)
admin.site.register(Resident)
admin.site.register(Employee)
admin.site.register(InternalRegiment, InternalRegimentModelAdmin)
admin.site.register(Statute, StatuteModelAdmin)

admin.site.site_header = 'APVMA'
admin.site.index_title = 'APVMA'
admin.site.site_title = 'administração'