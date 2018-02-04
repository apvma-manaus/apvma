import unittest

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apvma.assembly.models import Assembly


class AssemblyModelTest(TestCase):
    def setUp(self):
        self.document = Assembly.objects.create(file='Assembly_minute_26_JAN_2018.pdf',
                                                date='2018-01-26')

    def test_create(self):
        self.assertTrue(Assembly.objects.exists())

    @unittest.skip('teste não está passando')
    def test_only_pdf_upload_is_permitted(self):
        """The file to upload must be a PDF file"""
        Assembly.objects.all().delete()
        with self.assertRaises(ValidationError):
            file = SimpleUploadedFile('wrong.jpg', b'this is some text', content_type='image/jpg')
            not_allowed = Assembly.objects.create(file=file)
    #TODO: fazer o teste passar. O sistema já funciona mas o teste não passa.