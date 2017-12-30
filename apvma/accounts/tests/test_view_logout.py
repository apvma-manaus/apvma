from django.test import TestCase
from django.shortcuts import resolve_url as r


class LogOutViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('logout'))

    def test_get(self):
        self.assertRedirects(self.resp, r('login'))