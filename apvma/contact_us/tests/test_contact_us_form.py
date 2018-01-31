from django.core.exceptions import ValidationError
from django.test import TestCase

from apvma.contact_us.forms import ContactUsForm


class ContactUsFormTests(TestCase):
    def test_form_has_fields(self):
        """form must have 1 field: content"""
        form = ContactUsForm()
        expected = ['content', 'identify', 'file']
        self.assertEqual(expected, list(form.fields))

    def test_content_field_required(self):
        """Content field must be required"""
        form = self.make_validated_form(content='')
        self.assertRaises(ValidationError)

    def test_identify_field_required(self):
        """One identification option must be selected"""
        form = self.make_validated_form(identify='')
        self.assertRaises(ValidationError)

    def test_file_field_not_required(self):
        """Upload file is optional"""
        form = self.make_validated_form(file='')
        self.assertFalse(form.errors)

    def make_validated_form(self, **kwargs):
        valid = dict(content='This is a message.', identify='1', file='file.jpg')
        data = dict(valid, **kwargs)
        form = ContactUsForm(data)
        form.is_valid()
        return form
