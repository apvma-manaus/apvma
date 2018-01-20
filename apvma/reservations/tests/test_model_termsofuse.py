from django.core.exceptions import ValidationError
from django.test import TestCase

from apvma.reservations.models import TermsOfUse


class TermsOfUseModelTest(TestCase):
    def setUp(self):
        self.termsofuse = TermsOfUse.objects.create(file='TermsOfUse.pdf')

    def test_create(self):
        self.assertTrue(TermsOfUse.objects.exists())

    def test_model_has_only_one_instance(self):
        """The model must have only 1 instance"""
        with self.assertRaises(ValidationError):
            TermsOfUse.objects.create(file='TermsOfUse_2.pdf')

    # def test_only_pdf_upload_is_permitted(self):
    #     """The file to upload must be a PDF file"""
    #     with self.assertRaises(ValidationError):
    #         TermsOfUse.objects.all().delete()
    #         not_allowed = TermsOfUse.objects.create(file='WrongFile.doc')

    #TODO: fazer o teste passar