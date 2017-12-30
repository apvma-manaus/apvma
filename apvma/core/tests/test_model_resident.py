from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from apvma.core.models import Resident


class ResidentModelTests(TestCase):
    def setUp(self):
        self.apartment = User.objects.create(username='RS603', password='123456')
        self.resident = Resident.objects.create(
                            post='MJ', full_name='Bruno Luiz Santana de Araujo',
                            war_name='Santana', cpf='12345678901',
                            email='santanablsa@fab.mil.br', apartment=self.apartment
                        )

    def test_create(self):
        self.assertTrue(Resident.objects.exists())

    def test_post_choices(self):
        """Post choices should be limited to CL, TCL, MJ, CP, 1T e 2T"""
        apartment2 = User.objects.create(username='RS604', password='654321')
        resident2 = Resident.objects.create(
                        post='AA', full_name='Bruno Luiz Santana de Araujo',
                        war_name='Santana', cpf='12345678901',
                        email='santanablsa@fab.mil.br', apartment=apartment2
                        )
        self.assertRaises(ValidationError, resident2.full_clean)
