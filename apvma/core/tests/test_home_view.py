from django.test import TestCase
from django.shortcuts import resolve_url as r


# class HomeViewTest(TestCase):
#     def setUp(self):
#         self.resp = self.client.get(r('home'))
#
#     def test_get(self):
#         self.assertEqual(200, self.resp.status_code)
#
#     def test_template(self):
#         self.assertTemplateUsed(self.resp, 'index.html')