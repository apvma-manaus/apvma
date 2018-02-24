from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Visitor(models.Model):
    datetime = models.DateTimeField('estimada de chegada')
    description = models.TextField('nome / descrição', max_length=50)
    arrival_date = models.DateField('data_chegada', blank=True, null=True)
    arrival_time = models.TimeField('hora chegada', blank=True, null=True)
    exit_date = models.DateField('saída', blank=True, null=True)
    exit_time = models.TimeField('saída', blank=True, null=True)
    card = models.PositiveIntegerField('cartão', blank=True, null=True, validators=[MinValueValidator(1),
                                                                                    MaxValueValidator(60)])
    user = models.ForeignKey(User,verbose_name='apartamento', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Visita Autorizada'
        verbose_name_plural = 'Visitas Autorizadas'
        ordering = ('-datetime', 'user', 'description')

    def save(self, *args, **kwargs):
        '''Auto save for arrival_date and exit_date when changing arrival_time and exit_time'''
        if self.arrival_time and not self.arrival_date:
            self.arrival_date = datetime.today()
        if self.exit_time and not self.exit_date:
            self.exit_date = datetime.today()

        return super(Visitor, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        """It must have a card when it has an arrival_date.
           Minimum card number: 1, Maximum card number: 60"""
        if self.arrival_time and not self.card:
            raise ValidationError('Selecione o cartão alocado para o visitante.')
        if self.arrival_time and self.card not in range(1, 61):
            raise ValidationError('Número de cartão inexistente. Cartões existentes: 1 a 60.')