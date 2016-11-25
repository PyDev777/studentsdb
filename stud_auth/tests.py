from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
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


@override_settings(LANGUAGE_CODE='en')
class TestUserProfileForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()
        # remember url to edit form
        self.url = reverse('profile')

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
        self.assertEqual(response.redirect_chain[0], ('http://testserver/users/login/?next=/users/profile/', 302))

    def test_form(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('form', response.content)
        self.assertIn('username', response.content)
        self.assertIn('first_name', response.content)
        self.assertIn('last_name', response.content)
        self.assertIn('photo', response.content)
        self.assertIn('mobile_phone', response.content)
        self.assertIn('address', response.content)
        self.assertIn('name="save_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('You want to change the password?', response.content)

    def test_styles(self):
        # login as admin to access student edit form
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


class StProfileModelTests(TestCase):
    """Test event model"""

    def test_unicode(self):
        user = User(username='user1', email='test@test.com')
        st_user = StProfile(user=user, mobile_phone='355-355')
        self.assertEqual(unicode(st_user), u'user1')

