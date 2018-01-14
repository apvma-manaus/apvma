from django.db import models
from django.db.models import Q
from django.utils import timezone


class ValidReservationManager(models.Manager):
    """Query for valid reservations: not canceled and ((not paid and not expired) or paid)"""
    def get_queryset(self):
        now = timezone.now()
        return super(ValidReservationManager, self).get_queryset().filter(
            Q(canceled=False), Q(paid=False, expires_on__gt=now) | Q(paid=True))

#TODO: filtrar reservas válidas para passar para o template. Aparecer apenas reservas válidas no calenário
