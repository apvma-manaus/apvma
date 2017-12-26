from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r

from apvma.accounts.forms import SignUpForm


class SignUpViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('signup'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'signup.html')

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.resp.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        contents = [
            ('<input', 5),
            ('type="text"', 1),
            ('type="email"', 1),
            ('type="password"', 2)
        ]
        for content, number in contents:
            with self.subTest():
                self.assertContains(self.resp, content, number)



class SuccessfulSign_upTests(TestCase):
    def setUp(self):
        url = r('signup')
        data = {
            'username': 'bruno',
            'email': 'santanasta@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.resp = self.client.post(url, data)
        self.home_url = r('home')

    def test_redirection(self):
        """A valid form submission should redirect the user to the home page"""
        self.assertRedirects(self.resp, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSign_upTests(TestCase):
    def setUp(self):
        url = r('signup')
        self.resp = self.client.post(url, {}) #submit an empty dictionary

    def test_sign_up_status_code(self):
        """An invalid form submission should return to the same page"""
        self.assertEqual(200, self.resp.status_code)

    def test_form_errors(self):
        form = self.resp.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())