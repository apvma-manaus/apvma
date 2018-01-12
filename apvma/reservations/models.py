from django.contrib.auth.models import User
from django.db import models


class Reservation(models.Model):
    SPOTS = (
        ('TP', 'Tapiri'),
        ('SF', 'Salão de Festas')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('data')
    spot = models.CharField('ambiente', max_length=2, choices=SPOTS)
    created_on = models.DateTimeField('data da solicitação', auto_now_add=True)
    paid = models.BooleanField('pago', default=False)
    canceled = models.BooleanField('cancelado', default=False)
    canceled_on = models.DateTimeField('cancelado em', blank=True, null=True)
    expired = models.BooleanField('expirado', default=False)

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ('date',)

    def __str__(self):
        return '{} - {} - {}'.format(self.user.username, self.date, self.spot)

    def get_color(self):
        """Defines the background color of each reservation line in the table"""
        if self.canceled or self.expired:
            return '#FF9A84' #red
        elif self.paid:
            return '#9FFF99' #green
        else:
            return 'white'

    @property
    def status(self):
        """Defines the status of the reservation:
        when a reservation is created, it returns 'aguardando pagamento'
        when a reservation is canceled, it returns 'cancelada em '+ data de cancelamento'
        when a reservation is expired, it returns 'expirada por falta de pagamento'
        when a reservation is paid, it returns 'reserva confirmada'"""
        if self.canceled:
            return 'cancelada em {}'.format(self.canceled_on.date().strftime('%d/%m/%Y'))
        elif self.expired:
            return 'expirada por falta de pagamento'
        elif self.paid:
            return 'confirmada'
        else:
            return 'aguardando pagamento'
