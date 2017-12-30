from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

from apvma.accounts.forms import RequestSignUpForm


class RequestSignUpGet(TestCase):
    """Tests for GET method"""
    def setUp(self):
        self.resp = self.client.get(r('request_signup'))
        self.form = self.resp.context['form']

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template accounts/templates/request_signup.html"""
        self.assertTemplateUsed(self.resp, 'request_signup_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 5),
                ('type="text"', 3),
                ('<select', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have RequestSignUpForm form"""
        self.assertIsInstance(self.form, RequestSignUpForm)


class RequestSignUpPostValid(TestCase):
    """Tests for Valid POST"""
    def setUp(self):
        self.data = dict(post='MJ', full_name='Bruno Luiz Santana de Araujo',
                         war_name='Santana', cpf='12345678901', email='santana@fab.mil.br',
                         block='RS', apt_number='603')
        self.resp = self.client.post(r('request_signup'), self.data)

    def test_send_subscribe_email(self):
        """System must send email to APVMA after request"""
        self.assertEqual(1, len(mail.outbox))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'request_signup_done.html')

    def test_html_message(self):
        """Html must show message after request signup"""
        expected = [
            'Solicitação de cadastro realizada com sucesso!',
            'Aguarde que em breve entraremos em contato com você',
            'APVMA'
        ]
        with self.subTest():
            for text in expected:
                self.assertContains(self.resp, text)


class RequestSignUpPostInvalid(TestCase):
    """Tests for Invalid POST"""
    def setUp(self):
        self.resp = self.client.post(r('request_signup'), {})
        self.form = self.resp.context['form']

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use request_signup_form.html"""
        self.assertTemplateUsed(self.resp, 'request_signup_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, RequestSignUpForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(post='MJ', full_name='Bruno Luiz Santana de Araujo')
        response = self.client.post(r('request_signup'), invalid_data)

        self.assertContains(response, '<div class="invalid-feedback">')