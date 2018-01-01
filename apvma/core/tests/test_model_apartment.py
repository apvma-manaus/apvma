# from django.core.exceptions import ValidationError
# from django.db import IntegrityError
# from django.test import TestCase
#
# from apvma.core.models import Apartment
#
#
# class ApartmentModelTest(TestCase):
#     def setUp(self):
#         self.apt = Apartment.objects.create(block='RN', number='101')
#
#     def test_create(self):
#         self.assertTrue(Apartment.objects.exists)
#
#     def test_block_choices(self):
#         """Block must be RN, RS, RA or RJ"""
#         apt2 = Apartment.objects.create(block='AA', number='101')
#         self.assertRaises(ValidationError, apt2.full_clean)
#
#     def test_number_choices(self):
#         """Number must start with 1, 2, 3, 4, 5 or 6 and end with 01, 02, 03 or 04"""
#         apt3 = Apartment.objects.create(block='RN', number='105')
#         self.assertRaises(ValidationError, apt3.full_clean)
#
#     def test_nuiqueness(self):
#         """Block and number together must be unique (ex.: RN-101)"""
#         with self.assertRaises(IntegrityError):
#             apt_already_exists = Apartment.objects.create(block='RN', number='101')