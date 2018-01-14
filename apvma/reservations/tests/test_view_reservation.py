from datetime import datetime
from freezegun import freeze_time


import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.reservations.models import Reservation


@freeze_time('2018-01-10')
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

    def test_html(self):
        """Html must contain 3 titles: Minhas reservas, Disponibilidade and Faça sua reserva """
        titles = ['Minhas reservas', 'Disponibilidade', 'Faça sua reserva']
        with self.subTest():
            for title in titles:
                self.assertContains(self.resp, title)

    def test_html_has_calendar(self):
        """Html must show a calendar"""
        weekdays = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        with self.subTest():
            for day in weekdays:
                self.assertContains(self.resp, day)

    def test_html_calendar_must_have_link_to_next_and_previous_month(self):
        """Calendar must have previous month and next month link"""
        links = ['<a href="/reservations/2017/12/">« Mês anterior</a>',
                 '<a href="/reservations/2018/2/">Próximo mês »</a>']
        with self.subTest():
            for link in links:
                self.assertContains(self.resp, link)



class ResevationViewNotLoggedTest(TestCase):
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
            user=self.user, date='2018-01-21', spot='Tapiri'
        )
        self.resp = self.client.get(r('reservations'))

    def test_context(self):
        reservation = self.resp.context['reservations'][0]
        self.assertIsInstance(reservation, Reservation)

    def test_has_reservation(self):
        expected = ['DATA', 'LOCAL', 'SITUAÇÃO DA RESERVA',
                    '21 de Janeiro de 2018', 'Domingo', 'Tapiri']
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
        reservation2 = Reservation.objects.create(
            user=self.user, date='2018-01-22', spot='Tapiri'
        )
        reservation2.canceled = True
        reservation2.canceled_on = datetime(2018, 1, 11, 12, 0, 0, tzinfo=pytz.UTC)
        reservation2.save()
        resp = self.client.get(r('reservations'))
        expected = 'cancelada em 11/01/2018'
        self.assertContains(resp, expected)

    def test_reservation_expired(self):
        """Reservation must expire in 48h if the user doesn't pay it"""
        reservation3 = Reservation.objects.create(
            user=self.user, date='2018-01-23', spot='Tapiri'
        )
        reservation3.created_on = datetime(2018, 1, 7, 12, 0, 0, tzinfo=pytz.UTC)
        reservation3.save()
        resp = self.client.get(r('reservations'))
        expected = 'expirada por falta de pagamento'
        self.assertContains(resp, expected)

    def test_reservation_paid_doesnt_expire(self):
        """Reservation paid does not expire"""
        reservation4 = Reservation.objects.create(
            user=self.user, date='2018-01-24', spot='Tapiri'
        )
        reservation4.created_on = datetime(2018, 1, 7, 12, 0, 0, tzinfo=pytz.UTC)
        reservation4.paid = True
        reservation4.save()
        resp = self.client.get(r('reservations'))
        expected = 'confirmada'
        self.assertContains(resp, expected)
