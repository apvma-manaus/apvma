from django.contrib.auth.models import User
from django.test import TestCase

from apvma.core.models import Employee


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='antonio', password='123456')
        self.employee = Employee.objects.create(
            full_name='Antonio José da Silva', cpf='12345678901',
            birth_date='1990-01-30', user=self.user
        )

    def test_create(self):
        self.assertTrue(Employee.objects.exists())

