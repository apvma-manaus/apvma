from datetime import time, date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from freezegun import freeze_time

from apvma.core.models import Apartment
from apvma.visitors.models import Visitor


@freeze_time('2018-02-20')
class VisitorsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bruno', password='1234')
        self.visitor = Visitor.objects.create(datetime='2018-02-20 12:00',
                                              description='Fogás entrega de gás',
                                              user=self.user)

    def test_create(self):
        self.assertTrue(Visitor.objects.exists())

    def test_card_when_arrival(self):
        """There must be a card when an arrival exists"""
        with self.assertRaises(ValidationError):
            self.visitor.arrival_time = time(17, 20)
            self.visitor.full_clean()
            self.visitor.save()

    def test_card_positive_number(self):
        """Minimum card number must be 1"""
        with self.assertRaises(ValidationError):
            self.visitor.arrival_time = time(17, 20)
            self.visitor.card = 0
            self.visitor.full_clean()
            self.visitor.save()

    def test_card_maximum_60(self):
        """Maximum card_number must be 60"""
        with self.assertRaises(ValidationError):
            self.visitor.arrival_time = time(17, 20)
            self.visitor.card = 61
            self.visitor.full_clean()
            self.visitor.save()

    def test_auto_arrival_date(self):
        """When setting an arrival_time, arrival_date must be today"""
        self.visitor.arrival_time = time(17, 20)
        self.visitor.card = 1
        self.visitor.save()
        visitor = Visitor.objects.get(pk=1)
        self.assertEqual(visitor.arrival_date, date(2018, 2, 20))

    def test_auto_exit_date(self):
        """When setting an exit_time, exit_date must be today"""
        self.visitor.exit_time = time(19, 30)
        self.visitor.save()
        visitor = Visitor.objects.get(pk=1)
        self.assertEqual(visitor.exit_date, date(2018, 2, 20))

