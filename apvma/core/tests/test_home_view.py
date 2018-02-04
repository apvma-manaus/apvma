from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.core.models import InternalRegiment, Statute


class HomeViewLoggedTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.internal_regiment = InternalRegiment.objects.create(file='regimento_interno.pdf')
        self.statute = Statute.objects.create(file='estatuto.pdf')
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

    def test_links_to_regimento_interno_and_estatuto(self):
        """Html must contain link to the 'regimento interno' (Internal Regiment of the village)
        and to the 'estatuto' (Statute of APVMA)"""
        expected = [('Regimento Interno', 1),
                    ('Estatuto', 1),
                    ('<embed src="', 2),
                    (self.internal_regiment.file.url, 1),
                    (self.statute.file.url, 1)]
        for text, count in expected:
            with self.subTest():
                self.assertContains(self.resp, text, count)

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