from django.test import TestCase

from apvma.accounts.forms import RequestSignUpForm


class RequestSignUpFormTests(TestCase):
    def setUp(self):
        self.form = RequestSignUpForm()

    def test_has_fields(self):
        """Form must have 7 fields:
        post, full_name, war_name, cpf, email, block, apt_number"""
        expected = ['post', 'full_name', 'war_name', 'cpf', 'email', 'block', 'apt_number']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits."""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_full_name_must_be_titled(self):
        """Full Name must be titled"""
        form = self.make_validated_form(full_name='BRUNO luiz santana DE ARAUJO')
        self.assertEqual('Bruno Luiz Santana De Araujo', form.cleaned_data['full_name'])

    def test_war_name_must_be_uppercase(self):
        """War Name must be upper case"""
        form = self.make_validated_form(war_name='sanTAnA')
        self.assertEqual('SANTANA', form.cleaned_data['war_name'])

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(post='MJ', full_name='Bruno Luiz Santana de Araujo',
                     war_name='Santana', cpf='12345678901', email='santana@fab.mil.br',
                     block='RS', apt_number='603')
        data = dict(valid, **kwargs)
        form = RequestSignUpForm(data)
        form.is_valid()
        return form