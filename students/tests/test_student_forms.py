# from datetime import datetime
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from students.models import Student, Group


@override_settings(LANGUAGE_CODE='en')
class TestStudentUpdateForm(TestCase):

    fixtures = ['students_test_data.json']

    # @modify_settings
    # urls = 'studentsdb.test_urls'

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('students_edit', kwargs={'pk': 1})

    def test_form(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')
        # get form and check few fields there
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('Student edit', response.content)
        self.assertIn('Ticket', response.content)
        self.assertIn('Last Name', response.content)
        self.assertIn('name="save_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('podoba.jpg', response.content)

    def test_success(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        # TODO: post new photo for homework
        group = Group.objects.filter(title='Group2')[0]
        response = self.client.post(self.url, {
            'first_name': 'Updated Name', 'last_name': 'Updated Last Name', 'ticket': '567', 'student_group': group.id, 'birthday': '1990-11-11'
        }, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # test updated student details
        student = Student.objects.get(pk=1)
        self.assertEqual(student.first_name, 'Updated Name')
        self.assertEqual(student.last_name, 'Updated Last Name')
        self.assertEqual(student.ticket, '567')
        self.assertEqual(student.student_group, group)

        # check proper redirect after form post
        self.assertIn('Student updated successfully', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20updated%20successfully!')

    # def test_cancel(self):
    #     # login as admin to access student edit form
    #     self.client.login(username='admin', password='admin')
    #
    #     # post form with Cancel button
    #     response = self.client.post(self.url, {'cancel_button': 'Cancel'},
    #         follow=True)
    #
    #     self.assertIn('Student update canceled!', response.content)
    #     self.assertEqual(response.redirect_chain[0][0],
    #         'http://testserver/?status_message=' +
    #         'Student%20update%20canceled!')

    # def test_access(self):
    #     # try to access form as anonymous user
    #     response = self.client.get(self.url, follow=True)
    #
    #     # we have to get 200 code and login form
    #     self.assertEqual(response.status_code, 200)
    #
    #     # check that we're on login form
    #     self.assertIn('Login Form', response.content)
    #
    #     # check redirect url
    #     self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/students/1/edit/', 302))

    # def test_styles(self):
    #     # login as admin to access student edit form
    #     self.client.login(username='admin', password='admin')
    #
    #     # get form and check few fields there
    #     response = self.client.get(self.url)
    #
    #     # check response status
    #     self.assertEqual(response.status_code, 200)
    #
    #     # check classes
    #     self.assertIn('form-horizontal', response.content)
    #     self.assertIn('form-group', response.content)
    #     self.assertIn('control-label', response.content)
    #     self.assertIn('controls', response.content)
    #     self.assertIn('form-actions', response.content)
    #     self.assertIn('btn-primary', response.content)
