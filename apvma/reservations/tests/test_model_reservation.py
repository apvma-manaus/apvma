from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from apvma.reservations.models import Reservation


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.reservation = Reservation.objects.create(
            user=self.user, date='2018-01-10', spot='TP'
        )

    def test_create(self):
        self.assertTrue(Reservation.objects.exists())

    def test_nuiqueness(self):
        """One spot can not be reserved for two apartments at the same day"""
        with self.assertRaises(IntegrityError):
            reservation_already_exists = Reservation.objects.create(date='2018-01-10', spot='TP')
