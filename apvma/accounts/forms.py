from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apvma.core.models import Resident


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class RequestSignUpForm(forms.ModelForm):
    BLOCKS = (
        ('RN', 'Rio Negro'),
        ('RS', 'Rio Solimões'),
        ('RA', 'Rio Amazonas'),
        ('RJ', 'Rio Japurá')
    )
    block = forms.ChoiceField(label='Bloco', choices=BLOCKS)

    NUMBERS = (
        ('101', '101'), ('102', '102'), ('103', '103'), ('104', '104'),
        ('201', '201'), ('202', '202'), ('203', '203'), ('204', '204'),
        ('301', '301'), ('302', '302'), ('303', '303'), ('304', '304'),
        ('401', '401'), ('402', '402'), ('403', '403'), ('404', '404'),
        ('501', '501'), ('502', '502'), ('503', '503'), ('504', '504'),
        ('601', '601'), ('602', '602'), ('603', '603'), ('604', '604'),
    )
    apt_number = forms.ChoiceField(label='Apartamento nº', choices=NUMBERS)

    class Meta:
        model = Resident
        fields = ('post', 'full_name', 'war_name', 'cpf', 'email', 'block', 'apt_number')

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        return full_name.title()

    def clean_war_name(self):
        war_name = self.cleaned_data['war_name']
        return war_name.upper()

    def clean(self):
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(RequestSignUpForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            placeholders = [
                ('full_name', 'Digite aqui o nome completo'),
                ('war_name', 'Digite aqui o nome de guerra'),
                ('cpf', 'Digite apenas números'),
                ('email', 'Digite o e-mail ZIMBRA'),
            ]
            for field_name, placeholder in placeholders:
                if key == field_name:
                    field.widget.attrs.update({'placeholder': placeholder})