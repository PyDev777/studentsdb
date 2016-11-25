from django.core import mail
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from captcha.conf import settings as captcha_settings


@override_settings(LANGUAGE_CODE='en')
class ContactAdminTests(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        captcha_settings.CAPTCHA_TEST_MODE = True
        self.client = Client()
        self.url = reverse('contact_letter')

    def test_context(self):
        """Check context"""
        # prepare client and login as administrator
        self.client.login(username='admin', password='admin')

        response = self.client.get(self.url)

        self.assertIn('title', response.context)
        self.assertIn('Contact Administrator', response.content)

    def test_email_sent(self):
        """Check if email is being sent"""
        # prepare client and login as administrator
        self.client.login(username='admin', password='admin')

        # make form submit
        response = self.client.post(self.url, {
            'from_email': 'from@gmail.com',
            'subject': 'test email',
            'message': 'test email message',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        })

        # check if test email backend catched our email to admin
        msg = mail.outbox[0].message()
        self.assertEqual(msg.get('subject'), 'from@gmail.com send me: test email')
        # self.assertEqual(msg.get('from'), u'msg-sender@ukr.net')
        self.assertEqual(msg.get_payload(), 'test email message',)

    def test_cancel(self):
        """Check if email is being sent"""

        # prepare client and login as administrator
        self.client.login(username='admin', password='admin')

        # post form with Cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)

        self.assertIn('Letter sent canceled!', response.content)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/contact-admin/?status_message=' + 'Letter%20sent%20canceled!')

    def tearDown(self):
        captcha_settings.CAPTCHA_TEST_MODE = False
