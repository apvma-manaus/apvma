from django.contrib.auth.models import User
from rest_framework import serializers

from apvma.reservations.models import Reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Reservation
        fields = ('user', 'date', 'spot', 'created_on', 'status')
