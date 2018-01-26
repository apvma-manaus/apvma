from django import forms


class ContactUsForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)