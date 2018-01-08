from django.contrib import admin

from apvma.accountability.forms import AccountabilityAdminForm
from apvma.accountability.models import Accountability


class AccountabilityAdmin(admin.ModelAdmin):
    form = AccountabilityAdminForm


admin.site.register(Accountability, AccountabilityAdmin)