from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.core.models import InternalRegiment


class HomeViewLoggedTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.internal_regiment = InternalRegiment.objects.create(file='regimento_interno.pdf')
        self.resp = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home.html')

    def test_html_link_to_change_password(self):
        expected = 'href="/settings/password/"'
        self.assertContains(self.resp, expected)

    def test_html_has_apvma_image(self):
        expected = '<img src="/static/img/apvma.png"'
        self.assertContains(self.resp, expected)

    def test_link_to_regimento_interno(self):
        """Html must contain link to the 'regimento interno' (rules of the village)"""
        expected = ['Regimento Interno', '<embed src="', self.internal_regiment.file.url]
        for text in expected:
            with self.subTest():
                self.assertContains(self.resp, text)

    def test_link_to_accountability(self):
        expected = 'href="{}"'.format(r('accountability'))
        self.assertContains(self.resp, expected)

    def test_link_to_reservations(self):
        year = datetime.now().year
        month = datetime.now().month
        expected = 'href="{}"'.format(r('reservation_calendar', year, month))
        self.assertContains(self.resp, expected)

    def test_link_to_contact_us(self):
        expected = 'href="{}"'.format(r('contact_us'))
        self.assertContains(self.resp, expected)


class HomeViewNotLoggedTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('home')))