from django import forms

from apvma.reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'date', 'spot']