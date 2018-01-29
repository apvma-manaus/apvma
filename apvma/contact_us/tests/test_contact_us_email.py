from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

from apvma.core.models import Apartment, Resident


class ContactUsNewPostValidIdentified(TestCase):
    """Tests for valid posts identified"""
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.client.login(username='usuario', password='password')
        self.apartment = Apartment.objects.create(block='RN', number='101', user=self.user)
        self.resident = Resident.objects.create(
            post='MJ', full_name='Bruno Luiz Santana de Araujo',
            war_name='Santana', cpf='12345678901',
            email='santanablsa@fab.mil.br', apartment=self.apartment
        )
        self.data = dict(content='Mensagem de contato do usuário', identify='1')
        self.resp = self.client.post(r('contact_us'), self.data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /contact_us/"""
        self.assertRedirects(self.resp, r('contact_us'))

    def test_send_contactus_email(self):
        """System must send email to APVMA"""
        self.assertEqual(1, len(mail.outbox))

    def test_contact_us_email_subject(self):
        """Email subject must be 'Mensagem do "Entre em contato conosco'"""
        expected = 'Mensagem do "Entre em contato conosco"'
        self.assertEqual(expected, self.email.subject)

    def test_contact_us_email_from(self):
        """Email must be from the logged user"""
        expected = 'santanablsa@fab.mil.br'
        self.assertEqual(expected, self.email.from_email)

    def test_contact_us_email_to(self):
        """Email must be sent to APVMA"""
        expected = [settings.DEFAULT_APVMA_EMAIL]
        self.assertEqual(expected, self.email.to)

    def test_contact_us_email_body(self):
        """Email body must contain the Apartment and the Resident"""
        contents = ['usuario', 'MJ SANTANA']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)


class ContactUsNewPostValidAnonimous(TestCase):
    """Tests for valid posts anonimous"""
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.client.login(username='usuario', password='password')
        self.apartment = Apartment.objects.create(block='RN', number='101', user=self.user)
        self.resident = Resident.objects.create(
            post='MJ', full_name='Bruno Luiz Santana de Araujo',
            war_name='Santana', cpf='12345678901',
            email='santanablsa@fab.mil.br', apartment=self.apartment
        )
        self.data = dict(content='Mensagem de contato do usuário', identify='2')
        self.resp = self.client.post(r('contact_us'), self.data)
        self.email = mail.outbox[0]

    def test_contact_us_email_body(self):
        """Email body must not contain the Apartment and the Resident"""
        contents = ['usuario', 'MJ SANTANA']
        for content in contents:
            with self.subTest():
                self.assertNotIn(content, self.email.body)