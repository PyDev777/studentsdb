from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from students.models import Student, Group


@override_settings(LANGUAGE_CODE='en')
class TestGroupUpdateForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('groups_edit', kwargs={'pk': 1})

    def test_access(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check that we're on login form
        self.assertIn('form', response.content)
        self.assertIn('username', response.content)
        self.assertIn('password', response.content)

        # check redirect url
        self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/groups/1/edit/', 302))

    def test_cancel(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with Cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)

        self.assertIn('Group update canceled!', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20update%20canceled!')

    def test_fail_leader(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        url = reverse('groups_edit', kwargs={'pk': 2})
        student = Student.objects.get(pk=1)
        response = self.client.post(url, {'title': 'Title', 'leader': student.id, 'notes': 'Invalid leader'}, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check proper redirect after form post
        self.assertIn('Please, correct the following errors', response.content)

    def test_form(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('Group edit', response.content)
        self.assertIn('name="save_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)

    def test_styles(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check classes
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)
        self.assertIn('control-label', response.content)
        self.assertIn('controls', response.content)
        self.assertIn('btn-primary', response.content)

    def test_success(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        student = Student.objects.get(pk=1)
        response = self.client.post(self.url, {'title': 'Updated Title', 'leader': student.id, 'notes': 'No notes'}, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # test updated group details
        group = Group.objects.get(pk=1)
        self.assertEqual(group.title, 'Updated Title')
        self.assertEqual(group.leader.id, student.id)
        self.assertEqual(group.notes, 'No notes')

        # check proper redirect after form post
        self.assertIn('Group updated successfully', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20updated%20successfully!')


@override_settings(LANGUAGE_CODE='en')
class TestGroupAddForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('groups_add')

    def test_access(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check that we're on login form
        self.assertIn('form', response.content)
        self.assertIn('username', response.content)
        self.assertIn('password', response.content)

        # check redirect url
        self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/groups/add/', 302))

    def test_cancel(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with Cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)

        self.assertIn('Group addition canceled!', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20addition%20canceled!')

    def test_form(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('Group add', response.content)
        self.assertIn('Title', response.content)
        self.assertIn('name="save_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)

    def test_success(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        student = Student.objects.get(pk=3)
        response = self.client.post(self.url, {'title': 'Added Title', 'leader': student.id, 'notes': 'Added'}, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # test updated group details
        group = Group.objects.filter(title='Added Title')[0]
        self.assertEqual(group.leader.id, student.id)
        self.assertEqual(group.notes, 'Added')

        # check proper redirect after form post
        self.assertIn('Group added successfully', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20added%20successfully!')

    def test_styles(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check classes
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)
        self.assertIn('control-label', response.content)
        self.assertIn('controls', response.content)
        self.assertIn('btn-primary', response.content)


@override_settings(LANGUAGE_CODE='en')
class TestGroupDeleteForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('groups_delete', kwargs={'pk': 3})

    def test_access(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check that we're on login form
        self.assertIn('form', response.content)
        self.assertIn('username', response.content)
        self.assertIn('password', response.content)

        # check redirect url
        self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/groups/3/delete/', 302))

    def test_cancel(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # post form with Cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)

        self.assertIn('Group deletion canceled!', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20deletion%20canceled!')

    def test_form(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('form', response.content)
        self.assertIn('Delete Group', response.content)
        self.assertIn('name="submit_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)

    def test_styles(self):
        # login as admin to access group edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check classes
        self.assertIn('form-horizontal', response.content)
        self.assertIn('btn-danger', response.content)
        self.assertIn('btn-default', response.content)

    def test_success(self):
        # login as admin to access group delete form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        response = self.client.post(self.url, {}, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check proper redirect after form post
        self.assertIn('Group deleted successfully', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/groups/?status_message=' + 'Group%20deleted%20successfully!')
