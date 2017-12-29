from django.test import TestCase

from apvma.accounts.forms import SignUpForm


class SignUpFormTest(TestCase):
    def setUp(self):
        self.form = SignUpForm()

    def test_form_has_fields(self):
        expected = ['username', 'password1', 'password2']
        actual = list(self.form.fields)
        self.assertSequenceEqual(expected, actual)