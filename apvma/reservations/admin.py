from django.contrib import admin

from apvma.reservations.models import Reservation


class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'spot', 'user', 'created_on', 'status')
    search_fields = ('date', 'spot', 'user')
    list_filter = ('spot', 'user')
    fields = ('user', 'date', 'spot', 'paid', 'canceled')
    ordering = ('-date', 'spot')

admin.site.register(Reservation, ReservationModelAdmin)