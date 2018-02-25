from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse

from apvma.accountability.models import Accountability


class AccountabilityViewLoggedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.group = Group.objects.create(name='permissionários')
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='usuario', password='password')
        self.accountability = Accountability.objects.create(date='2018-01-01', file='DEZ_2018.pdf')
        self.resp = self.client.get(r('accountability'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'accountability/accountability.html')

    def test_html(self):
        """Html must contain links to the accountabilities files"""
        with self.subTest():
            expected = ['2018/Janeiro', '<embed src="', self.accountability.file.url]
            for text in expected:
                self.assertContains(self.resp, text)


class AccountabilityViewNotLoggedTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accountability'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('accountability')))