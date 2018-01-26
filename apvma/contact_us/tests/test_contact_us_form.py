from django.test import TestCase

from apvma.contact_us.forms import ContactUsForm


class ContactUsFormTests(TestCase):
    def test_form_has_fields(self):
        """form must have 1 field: content"""
        form = ContactUsForm()
        expected = ['content']
        self.assertEqual(expected, list(form.fields))