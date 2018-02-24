from django import forms
from apvma.visitors.models import Visitor


class AuthorizeVisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['datetime', 'description']
