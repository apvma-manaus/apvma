from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apvma.core.models import Resident


class ResidentInLine(admin.StackedInline):
    model = Resident
    insert_after = 'password'
    verbose_name_plural = 'Permissionário'


class CustomUserAdmin(UserAdmin):
    inlines = [ResidentInLine,]
    list_display = ('username', 'resident')
    change_form_template = 'admin/custom/change_form.html'

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