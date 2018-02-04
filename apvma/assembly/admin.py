from django.contrib import admin

from apvma.assembly.models import Assembly


class AssemblyModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'file')
    ordering = ('-date',)


admin.site.register(Assembly, AssemblyModelAdmin)