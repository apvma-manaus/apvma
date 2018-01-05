from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apvma.core.models import Resident, Apartment


class ApartmentInLine(admin.TabularInline):
    model = Apartment
    insert_after = 'password'
    verbose_name = 'Apartamento'


class CustomUserAdmin(UserAdmin):
    #inlines = [ResidentInLine,]
    list_display = ('username',)

    def get_readonly_fields(self, request, obj=None):
        '''Impede de mudar o username do User ao editar o objeto'''
        if obj:
            return self.readonly_fields + ('username',)
        return self.readonly_fields

    def get_actions(self, request):
        '''Impede de apagar usuário pela tela principal'''
        actions = super(CustomUserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        '''Impede de apagar usuário pela tela de edição do usuário'''
        return False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Apartment)
admin.site.register(Resident)