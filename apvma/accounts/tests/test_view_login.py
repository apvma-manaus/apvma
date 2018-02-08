from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse


class LogInViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('login'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'login.html')

    def test_link_to_request_signup(self):
        expected = '<a href="/request_signup/"'
        self.assertContains(self.resp, expected)

    def test_html_has_apvma_image(self):
        expected = '<img src="/static/img/apvma.png"'
        self.assertContains(self.resp, expected)


class IndextTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('index'))

    def test_redirects_to_home(self):
        self.assertEqual(302, self.resp.status_code)
        #TODO: testar o redirecionamento para home