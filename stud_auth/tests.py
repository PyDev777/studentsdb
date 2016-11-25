from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from students.models import Student, Group
from stud_auth.models import StProfile, User


@override_settings(LANGUAGE_CODE='en')
class TestCustRegFormUniqEmail(TestCase):

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('users:registration_register')

    def test_form(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check form content
        self.assertIn('Registration Form', response.content)
        self.assertIn('form', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('username', response.content)
        self.assertIn('email', response.content)
        self.assertIn('password1', response.content)
        self.assertIn('password2', response.content)
        self.assertIn('captcha', response.content)
        self.assertIn('name="submit_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)

        # check form styles
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)
        self.assertIn('control-label', response.content)
        self.assertIn('controls', response.content)
        self.assertIn('btn-primary', response.content)


        # response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
        #
        # self.assertIn('Student update canceled!', response.content)
        # self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20update%20canceled!')


@override_settings(LANGUAGE_CODE='en')
class TestCustPswResetForm(TestCase):

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('password_reset')

    def test_form(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check form content
        self.assertIn('Reset password', response.content)
        self.assertIn('form', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('email', response.content)
        self.assertIn('captcha', response.content)
        self.assertIn('name="submit_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)

        # check form styles
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)
        self.assertIn('control-label', response.content)
        self.assertIn('controls', response.content)
        self.assertIn('btn-primary', response.content)


@override_settings(LANGUAGE_CODE='en')
class TestCustPswChangeForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('password_change')

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
        self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/users/password_change/', 302))

    def test_form(self):
        self.client.login(username='admin', password='admin')

        # try to access form as auth user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check form content
        self.assertIn('Change password', response.content)
        self.assertIn('form', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('new_password1', response.content)
        self.assertIn('new_password2', response.content)
        self.assertIn('old_password', response.content)
        self.assertIn('name="submit_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)

        # check form styles
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)
        self.assertIn('control-label', response.content)
        self.assertIn('controls', response.content)
        self.assertIn('btn-primary', response.content)




# @override_settings(LANGUAGE_CODE='en')
# class TestStudentUpdateForm(TestCase):
#
#     fixtures = ['students_test_data.json']
#
#     def setUp(self):
#         # remember test browser
#         self.client = Client()
#         # remember url to edit form
#         self.url = reverse('students_edit', kwargs={'pk': 1})
#
#     def test_access(self):
#         # try to access form as anonymous user
#         response = self.client.get(self.url, follow=True)
#
#         # we have to get 200 code and login form
#         self.assertEqual(response.status_code, 200)
#
#         # check that we're on login form
#         self.assertIn('form', response.content)
#         self.assertIn('username', response.content)
#         self.assertIn('password', response.content)
#
#         # check redirect url
#         self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/students/1/edit/', 302))
#
#     def test_cancel(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with Cancel button
#         response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
#
#         self.assertIn('Student update canceled!', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20update%20canceled!')
#
#     def test_fail_leader(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with valid data
#         # TODO: post new photo for homework
#         group = Group.objects.filter(title='Group2')[0]
#         response = self.client.post(self.url, {
#             'first_name': 'Updated Name', 'last_name': 'Updated Last Name', 'ticket': '567', 'student_group': group.id, 'birthday': '1990-11-11'
#         }, follow=True)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # check proper redirect after form post
#         self.assertIn('Student is the leader of another group!', response.content)
#
#     def test_form(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#
#         # check page title, few field titles and button on edit form
#         self.assertIn('Student edit', response.content)
#         self.assertIn('Ticket', response.content)
#         self.assertIn('Last Name', response.content)
#         self.assertIn('name="save_button"', response.content)
#         self.assertIn('name="cancel_button"', response.content)
#         self.assertIn('action="%s"' % self.url, response.content)
#         self.assertIn('podoba.jpg', response.content)
#
#     def test_styles(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # check classes
#         self.assertIn('form-horizontal', response.content)
#         self.assertIn('form-group', response.content)
#         self.assertIn('control-label', response.content)
#         self.assertIn('controls', response.content)
#         self.assertIn('btn-primary', response.content)
#
#     def test_success(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with valid data
#         # TODO: post new photo for homework
#         group = Group.objects.filter(title='Group1')[0]
#         response = self.client.post(self.url, {
#             'first_name': 'Updated Name', 'last_name': 'Updated Last Name', 'ticket': '567', 'student_group': group.id, 'birthday': '1990-11-11'
#         }, follow=True)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # test updated student details
#         student = Student.objects.get(pk=1)
#         self.assertEqual(student.first_name, 'Updated Name')
#         self.assertEqual(student.last_name, 'Updated Last Name')
#         self.assertEqual(student.ticket, '567')
#         self.assertEqual(student.student_group, group)
#
#         # check proper redirect after form post
#         self.assertIn('Student updated successfully', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20updated%20successfully!')
#
#
# @override_settings(LANGUAGE_CODE='en')
# class TestStudentAddForm(TestCase):
#
#     fixtures = ['students_test_data.json']
#
#     def setUp(self):
#         # remember test browser
#         self.client = Client()
#         # remember url to edit form
#         self.url = reverse('students_add')
#
#     def test_access(self):
#         # try to access form as anonymous user
#         response = self.client.get(self.url, follow=True)
#
#         # we have to get 200 code and login form
#         self.assertEqual(response.status_code, 200)
#
#         # check that we're on login form
#         self.assertIn('form', response.content)
#         self.assertIn('username', response.content)
#         self.assertIn('password', response.content)
#
#         # check redirect url
#         self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/students/add/', 302))
#
#     def test_cancel(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with Cancel button
#         response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
#
#         self.assertIn('Student addition canceled!', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20addition%20canceled!')
#
#     def test_form(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#
#         # check page title, few field titles and button on edit form
#         self.assertIn('Student add', response.content)
#         self.assertIn('Ticket', response.content)
#         self.assertIn('Last Name', response.content)
#         self.assertIn('name="save_button"', response.content)
#         self.assertIn('name="cancel_button"', response.content)
#         self.assertIn('action="%s"' % self.url, response.content)
#
#     def test_success(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with valid data
#         # TODO: post new photo for homework
#         group = Group.objects.filter(title='Group1')[0]
#         response = self.client.post(self.url, {
#             'first_name': 'Added Name', 'last_name': 'Added Last Name', 'ticket': '777', 'student_group': group.id, 'birthday': '1990-12-12'
#         }, follow=True)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # test updated student details
#         student = Student.objects.filter(last_name='Added Last Name')[0]
#         self.assertEqual(student.first_name, 'Added Name')
#         self.assertEqual(student.ticket, '777')
#         self.assertEqual(student.student_group, group)
#
#         # check proper redirect after form post
#         self.assertIn('Student added successfully', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20added%20successfully!')
#
#     def test_styles(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # check classes
#         self.assertIn('form-horizontal', response.content)
#         self.assertIn('form-group', response.content)
#         self.assertIn('control-label', response.content)
#         self.assertIn('controls', response.content)
#         self.assertIn('btn-primary', response.content)
#
#
# @override_settings(LANGUAGE_CODE='en')
# class TestStudentDeleteForm(TestCase):
#
#     fixtures = ['students_test_data.json']
#
#     def setUp(self):
#         # remember test browser
#         self.client = Client()
#         # remember url to edit form
#         self.url = reverse('students_delete', kwargs={'pk': 1})
#
#     def test_access(self):
#         # try to access form as anonymous user
#         response = self.client.get(self.url, follow=True)
#
#         # we have to get 200 code and login form
#         self.assertEqual(response.status_code, 200)
#
#         # check that we're on login form
#         self.assertIn('form', response.content)
#         self.assertIn('username', response.content)
#         self.assertIn('password', response.content)
#
#         # check redirect url
#         self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/students/1/delete/', 302))
#
#     def test_cancel(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # post form with Cancel button
#         response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
#
#         self.assertIn('Student deletion canceled!', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20deletion%20canceled!')
#
#     def test_form(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#
#         # check page title, few field titles and button on edit form
#         self.assertIn('form', response.content)
#         self.assertIn('Delete Student', response.content)
#         self.assertIn('name="submit_button"', response.content)
#         self.assertIn('name="cancel_button"', response.content)
#         self.assertIn('action="%s"' % self.url, response.content)
#
#     def test_styles(self):
#         # login as admin to access student edit form
#         self.client.login(username='admin', password='admin')
#
#         # get form and check few fields there
#         response = self.client.get(self.url)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # check classes
#         self.assertIn('form-horizontal', response.content)
#         self.assertIn('btn-danger', response.content)
#         self.assertIn('btn-default', response.content)
#
#     def test_success(self):
#         # login as admin to access student delete form
#         self.client.login(username='admin', password='admin')
#
#         # post form with valid data
#         response = self.client.post(self.url, {}, follow=True)
#
#         # check response status
#         self.assertEqual(response.status_code, 200)
#
#         # check proper redirect after form post
#         self.assertIn('Student deleted successfully', response.content)
#         self.assertEqual(response.redirect_chain[0][0], 'http://testserver/?status_message=' + 'Student%20deleted%20successfully!')


class StProfileModelTests(TestCase):
    """Test event model"""

    def test_unicode(self):
        user = User(username='user1', email='test@test.com')
        st_user = StProfile(user=user, mobile_phone='355-355')
        self.assertEqual(unicode(st_user), u'user1')
