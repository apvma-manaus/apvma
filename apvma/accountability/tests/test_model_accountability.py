from django.test import TestCase

from apvma.accountability.models import Accountability


class AccountabilityModelTest(TestCase):
    def setUp(self):
        Accountability.objects.create(date='2018-01-01', file='DEZ_2018.pdf')

    def test_create(self):
        self.assertTrue(Accountability.objects.exists())

#TODO: em produção, ocorre error 500 ao salvar o modelo