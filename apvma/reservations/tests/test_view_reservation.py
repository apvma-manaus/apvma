from datetime import datetime
from freezegun import freeze_time


import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.reservations.models import Reservation


class ReservationViewLoggedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.resp = self.client.get(r('reservations'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'reservations/reservations.html')

    def test_dont_have_reservations(self):
        expected = 'Você não possui reservas agendadas.'
        self.assertContains(self.resp, expected)


class ReservationViewNotLoggedTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('reservations'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('reservations')))


@freeze_time('2018-01-10')
class ReservartionViewContainReservation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.reservation = Reservation.objects.create(
            user=self.user, date='2018-01-15', spot='Tapiri'
        )
        self.resp = self.client.get(r('reservations'))

    def test_context(self):
        reservation = self.resp.context['reservations'][0]
        self.assertIsInstance(reservation, Reservation)

    def test_has_reservation(self):
        expected = ['DATA', 'AMBIENTE', 'SITUAÇÃO DA RESERVA',
                    '15 de Janeiro de 2018', 'Tapiri']
        with self.subTest():
            for text in expected:
                self.assertContains(self.resp, text)

    def test_reservation_not_paid(self):
        expected = 'aguardando pagamento'
        self.assertContains(self.resp, expected)

    def test_reservation_paid(self):
        self.reservation.paid = True
        self.reservation.save()
        resp = self.client.get(r('reservations'))
        expected = 'confirmada'
        self.assertContains(resp, expected)

    def test_reservation_canceled(self):
        self.reservation.canceled = True
        self.reservation.canceled_on = datetime(2018, 1, 12, 12, 0, 0, tzinfo=pytz.UTC)
        self.reservation.save()
        resp = self.client.get(r('reservations'))
        expected = 'cancelada em 12/01/2018'
        self.assertContains(resp, expected)