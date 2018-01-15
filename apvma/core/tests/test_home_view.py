from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse


class HomeViewLoggedTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='bruno', password='1234')
        self.client.login(username='bruno', password='1234')
        self.resp = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home.html')

    def test_html_link_to_change_password(self):
        expected = 'href="/settings/password/"'
        self.assertContains(self.resp, expected)

    def test_link_to_accountability(self):
        expected = 'href="{}"'.format(r('accountability'))
        self.assertContains(self.resp, expected)

    def test_link_to_reservations(self):
        expected = 'href="{}"'.format(r('reservations'))
        self.assertContains(self.resp, expected)


class HomeViewNotLoggedInTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('home')))