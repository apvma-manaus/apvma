from datetime import datetime, timezone, time

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.shortcuts import resolve_url as r, reverse
from freezegun import freeze_time

from apvma.core.models import Apartment, Resident
from apvma.visitors.forms import AuthorizeVisitorForm
from apvma.visitors.models import Visitor


class VisitorsViewNotLoggedTests(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('visitors'))

    def test_redirect(self):
        url = r('login')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('visitors')))


class VisitorsPermissionTests(TestCase):
    """Tests for visitors view permissions"""
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.client.login(username='usuario', password='password')
        self.resp = self.client.get(r('visitors'))

    def test_not_in_resident_group_no_access(self):
        """users not in 'permissionários' group should not access the visitors view"""
        url = r('home')
        self.assertRedirects(self.resp, '{}?next={}'.format(url, reverse('visitors')))


class VisitorsViewLoggedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.group = Group.objects.create(name='permissionários')
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='usuario', password='password')
        self.resp = self.client.get(r('visitors'))
        self.form = self.resp.context['form']

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'visitors/visitors.html')

    def test_html_has_two_sets(self):
        """Html must have 2 sets: 'Entradas autorizadas' and 'Autorizar entradas'"""
        sets = [
            'Entradas autorizadas por mim:',
            'Autorizar entrada:'
        ]
        for set in sets:
            with self.subTest():
                self.assertContains(self.resp, set)

    def test_html_with_no_visitors_planned(self):
        """Message if no visitors planned"""
        message = 'Você não possui entradas autorizadas.'
        self.assertContains(self.resp, message)

    def test_has_1_form(self):
        tags = (('<form', 1),
                ('type="submit"', 1))
        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form(self):
        """Context must have AuthorizeVisitorForm form"""
        self.assertIsInstance(self.form, AuthorizeVisitorForm)



    # def test_has_form(self):
    #     """Context must have AuthorizeVisitorsForm form"""
    #     self.assertIsInstance(self.form, AuthorizeVisitorsForm)


@freeze_time('2018-02-20')
class VisitorsViewVisitorsPlannedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.user2 = User.objects.create_user(username='usuario2', password='password2')
        self.apartment = Apartment.objects.create(block='RS', number='603', user=self.user)
        self.resident = Resident.objects.create(
            post='MJ', full_name='Bruno Luiz Santana de Araujo',
            war_name='Santana', cpf='12345678901',
            email='santanablsa@fab.mil.br', apartment=self.apartment
        )
        self.visitor = Visitor.objects.create(datetime=datetime(2018, 2, 20, 17, 0),
                                              description='Fogás entrega de gás',
                                              user=self.user)
        self.visitor_old = Visitor.objects.create(datetime=datetime(2018, 2, 19, 16, 0),
                                              description='Visita antiga',
                                              user=self.user)
        self.visitor2 = Visitor.objects.create(datetime=datetime(2018, 2, 21, 18, 0),
                                              description='Visita de outro morador',
                                              user=self.user2)
        self.group = Group.objects.create(name='permissionários')
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='usuario', password='password')
        self.resp = self.client.get(r('visitors'))

    def test_html_has_user_future_visitors_planned(self):
        """Html must show future visitors planned for the logged user"""
        contents = ['20/02/2018', '17:00 h', 'Fogás entrega de gás']
        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)

    def test_html_dont_have_other_user_visitors(self):
        """Html must not show other user visitors"""
        contents = ['21/02/2018', '18:00 h', 'Visita de outro morador']
        for content in contents:
            with self.subTest():
                self.assertNotContains(self.resp, content)

    def test_html_must_have_old_visitors_who_didnt_exit(self):
        """Html must show visitor who didn't exit yet"""
        contents = ['19/02/2018', '16:00 h', 'Visita antiga']
        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)

    def test_html_dont_have_old_visitors_who_exited(self):
        """Html must not show visitors planned for days before today"""
        self.visitor_old.arrival_time = time(16, 10)
        self.visitor_old.exit_time = time(18, 20)
        self.visitor_old.card = 1
        self.visitor_old.save()
        resp = self.client.get(r('visitors'))
        contents = ['19/02/2018', '16:00 h', 'Visita antiga']
        for content in contents:
            with self.subTest():
                self.assertNotContains(resp, content)

    def test_html_must_have_arrival_and_exit_time(self):
        """Html must show arrival and exit time of visitors of day equal or greater than today"""
        self.visitor.arrival_time = time(17, 10)
        self.visitor.exit_time = time(18, 30)
        self.visitor.card = 1
        self.visitor.save()
        resp = self.client.get(r('visitors'))
        contents = ['17:10 h', '18:30 h']

        for content in contents:
            with self.subTest():
                self.assertContains(resp, content)

    def test_has_cancel_visitor_authorization_form(self):
        tags = (('<form', 2),
                ('type="submit"', 2))
        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)


@freeze_time('2018-02-20')
class VisitorsPostCancelVisitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.apartment = Apartment.objects.create(block='RS', number='603', user=self.user)
        self.resident = Resident.objects.create(
            post='MJ', full_name='Bruno Luiz Santana de Araujo',
            war_name='Santana', cpf='12345678901',
            email='santanablsa@fab.mil.br', apartment=self.apartment
        )
        self.visitor = Visitor.objects.create(datetime=datetime(2018, 2, 20, 17, 0),
                                              description='Fogás entrega de gás',
                                              user=self.user)
        self.group = Group.objects.create(name='permissionários')
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='usuario', password='password')
        self.data = dict(cancel_authorization_button='', cancel_authorization=self.visitor.pk)
        self.resp = self.client.post(r('visitors'), self.data)

    def test_redirects(self):
        """Post cancel authorization should redirect to the same page"""
        self.assertRedirects(self.resp, r('visitors'))

    def test_visit_delete(self):
        """Visit canceled should be deleted"""
        self.assertFalse(Visitor.objects.exists())


@freeze_time('2018-02-20')
class VisitorsPostNewVisitTests(TestCase):
    """Tests to add new visit"""
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='password')
        self.apartment = Apartment.objects.create(block='RS', number='603', user=self.user)
        self.resident = Resident.objects.create(
            post='MJ', full_name='Bruno Luiz Santana de Araujo',
            war_name='Santana', cpf='12345678901',
            email='santanablsa@fab.mil.br', apartment=self.apartment
        )
        self.group = Group.objects.create(name='permissionários')
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='usuario', password='password')
        self.data = dict(new_authorization_button='', datetime='20/02/18 - 18:00', description='Nome da visita.')
        self.resp = self.client.post(r('visitors'), self.data)

    def test_redirects(self):
        """Post new authorization should redirect to the same page"""
        self.assertRedirects(self.resp, r('visitors'))

    def test_new_visit_create(self):
        """Post new authorization must create new visitor object"""
        self.assertTrue(Visitor.objects.exists())