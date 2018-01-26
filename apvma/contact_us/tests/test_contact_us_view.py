from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.contact_us.forms import ContactUsForm
from apvma.core.models import Apartment, Resident


class ContactUsViewNotLoggedTests(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('contact_us'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('contact_us')))


class ContactUsViewLoggedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.client.login(username='usuario', password='password')
        self.resp = self.client.get(r('contact_us'))
        self.form = self.resp.context['form']

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'contact_us/contact_us.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 1),
                ('<textarea', 1), # area to write the content
                ('type="submit"', 1)) # button to submit

        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have ContactUsForm form"""
        self.assertIsInstance(self.form, ContactUsForm)