from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse, resolve_url as r

from apvma.assembly.models import Assembly


class AssemblyViewNotLoggedTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('assembly'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('assembly')))


class AssemblyViewLoggedTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='usuario', password='password')
        self.client.login(username='usuario', password='password')
        self.assembly = Assembly.objects.create(file='assembly_minute_26_JAN_2018.pdf',
                                                date='2018-01-26')
        self.resp = self.client.get(r('assembly'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'assembly/assembly.html')

    def test_html(self):
        """Html must contain links to the assembly files"""
        expected = ['<embed src="', self.assembly.file.url]
        for text in expected:
            with self.subTest():
                self.assertContains(self.resp, text)

