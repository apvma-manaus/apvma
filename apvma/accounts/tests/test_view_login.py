from django.test import TestCase
from django.shortcuts import resolve_url as r


class LogInViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('login'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)