from django.core import mail
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class ContactAdminFormTests(TestCase):

    fixtures = ['students_test_data.json']

    def test_email_sent(self):
        """Check if email is being sent"""
        # prepare client and login as administrator
        client = Client()
        client.login(username='admin', password='admin')

        # make form submit
        response = client.post(reverse('contact_letter'), {
            'from_email': 'from@gmail.com',
            'subject': 'test email',
            'message': 'test email message'
        })

        # check if test email backend catched our email to admin
        msg = mail.outbox[0].message()
        self.assertEqual(msg.get('subject'), 'from@gmail.com send me: test email')
        self.assertEqual(msg.get('from'), u'msg-sender@ukr.net')
        self.assertEqual(msg.get_payload(), 'test email message',)
