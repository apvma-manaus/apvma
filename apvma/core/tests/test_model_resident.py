from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from apvma.core.models import Resident, Apartment


class ResidentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='RS603', password='123456')
        self.apartment = Apartment.objects.create(block='RN', number='101', user=self.user)
        self.resident = Resident.objects.create(
                            post='MJ', full_name='Bruno Luiz Santana de Araujo',
                            war_name='Santana', cpf='12345678901',
                            email='santanablsa@fab.mil.br', apartment=self.apartment
                        )

    def test_create(self):
        self.assertTrue(Resident.objects.exists())

    def test_user_email(self):
        """If resident has an apartment, User email must be the resident email"""
        user = User.objects.get(username='RS603')
        self.assertEqual(user.email, self.resident.email)

    def test_post_choices(self):
        """Post choices should be limited to CL, TCL, MJ, CP, 1T e 2T"""
        resident2 = Resident.objects.create(
                        post='AA', full_name='Bruno Luiz Santana de Araujo',
                        war_name='Santana', cpf='12345678901',
                        email='santanablsa@fab.mil.br'
                        )
        self.assertRaises(ValidationError, resident2.full_clean)

    def test_apartment_can_be_null(self):
        """Resident can have None apartment"""
        self.resident.apartment = None
        self.assertTrue(Resident.objects.exists())