from django.contrib import admin
from django.utils import timezone

from apvma.reservations.models import Reservation


class WaitingforPayment(admin.SimpleListFilter):
    """Filter in admin for reservations waiting for payment"""
    title = ('situação da reserva')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('aguardando pagamento', ('Aguardando pagamento')),
            ('confirmada', ('Confirmada')),
            ('cancelada', ('Cancelada')),
            ('expirada por falta de pagamento', ('Expirada por falta de pagamento'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'confirmada':
            return queryset.filter(paid=True, canceled=False)
        if self.value() == 'cancelada':
            return queryset.filter(canceled=True)
        if self.value() == 'aguardando pagamento':
            return queryset.filter(paid=False, canceled=False, expires_on__gt=timezone.now())
        if self.value() == 'expirada por falta de pagamento':
            return queryset.filter(paid=False, canceled=False, expires_on__lt=timezone.now())


class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'spot', 'user', 'created_on', 'status')
    search_fields = ('date', 'spot', 'user')
    list_filter = (WaitingforPayment, 'spot', 'user')
    fields = ('user', 'date', 'spot', 'paid', 'canceled')
    ordering = ('-date', 'spot')


admin.site.register(Reservation, ReservationModelAdmin)