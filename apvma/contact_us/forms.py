from django import forms


class ContactUsForm(forms.Form):
    CHOICES = (('1', 'Quero me identificar'),
               ('2', 'Quero que a mensagem seja anônima'))

    content = forms.CharField(widget=forms.Textarea)
    identify = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)