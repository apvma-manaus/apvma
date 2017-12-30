from django.contrib.auth.models import User
from django.db import models

from apvma.accounts.validators import validate_cpf


class Resident(models.Model):
    POSTS = (
        ('CL', 'Coronel'),
        ('TCL', 'Tenente-Coronel'),
        ('MJ', 'Major'),
        ('CP', 'Capitão'),
        ('1T', '1º Tenente'),
        ('2T', '2º Tenente')
    )

    post = models.CharField('posto', max_length=4, choices=POSTS)
    full_name = models.CharField('nome completo', max_length=100)
    war_name = models.CharField('nome de guerra', max_length=20)
    cpf = models.CharField('CPF', max_length=11, validators=[validate_cpf])
    email = models.EmailField('email intraer')
    apartment = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'morador'
        verbose_name_plural = 'moradores'

    def __str__(self):
        return ' '.join([self.post, self.war_name, '-', self.apartment])