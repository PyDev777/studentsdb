from django.test import TestCase

from stud_auth.models import StProfile, User


class StProfileModelTests(TestCase):
    """Test event model"""

    def test_unicode(self):
        user = User(username='user1', email='test@test.com')
        st_user = StProfile(user=user, mobile_phone='355-355')
        self.assertEqual(unicode(st_user), u'user1')
