from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class RequestSignUpMailTests(TestCase):
    """Tests for the request signup email"""
    def setUp(self):
        self.data = dict(post='MJ', full_name='Bruno Luiz Santana de Araujo',
                         war_name='Santana', cpf='12345678901', email='santana@fab.mil.br',
                         block='RS', apt_number='603')
        self.resp = self.client.post(r('request_signup'), self.data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """Email subject must be 'Confirmação de inscrição' """
        expect = 'Solicitação de cadastro de novo morador'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Email must be from santana@gmail.com"""
        expect = 'santana@fab.mil.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """Email must be sent to the user and to the sender"""
        expect = ['contatoapvma@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        """Email body must contain data from request form"""
        contents = [
            'MJ',
            'Bruno Luiz Santana De Araujo',
            'SANTANA',
            '123.456.789-01',
            'santana@fab.mil.br',
            'RS',
            '603'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)