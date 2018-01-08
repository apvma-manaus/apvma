from django import forms

from apvma.accountability.models import Accountability
from apvma.accountability.snippets.month_year_snippet import MonthYearWidget


class AccountabilityAdminForm(forms.ModelForm):

    class Meta:
        model = Accountability
        fields = ('date', 'file')
        widgets = {
            'date': MonthYearWidget(),
        }
