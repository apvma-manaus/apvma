from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from apvma.visitors.forms import AuthorizeVisitorForm


class AuthorizeVisitorFormTests(TestCase):
    def test_form_has_fields(self):
        """form must have 1 field: content"""
        form = AuthorizeVisitorForm()
        expected = ['datetime', 'description']
        self.assertEqual(expected, list(form.fields))

    def test_datetime_field_required(self):
        """Datetime field must be required"""
        form = self.make_validated_form(datetime='')
        self.assertTrue(form.errors)

    def test_identify_field_required(self):
        """Description field must be required"""
        form = self.make_validated_form(description='')
        self.assertTrue(form.errors)

    def make_validated_form(self, **kwargs):
        user = User.objects.create_user(username='usuario', password='password')
        valid = dict(datetime=datetime(2018, 2, 20, 17, 00), description='Descrição da visita.', user=user.pk)
        data = dict(valid, **kwargs)
        form = AuthorizeVisitorForm(data)
        form.is_valid()
        return form
