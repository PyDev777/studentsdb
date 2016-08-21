from django.test import TestCase
from ..models import Student, Group, MonthJournal, LogEntry
from studentsdb.models import StProfile, User


class StudentModelTests(TestCase):
    """Test student model"""

    def test_unicode(self):
        student = Student(first_name='Demo', last_name='Student')
        self.assertEqual(unicode(student), u'Demo Student')


class GroupModelTests(TestCase):
    """Test group model"""

    def test_unicode(self):
        group = Group(title='Demo Group')
        self.assertEqual(unicode(group), u'Demo Group')

    def test_unicode_leader(self):
        student = Student(first_name='Demo', last_name='Student')
        group = Group(title='Demo Group', leader=student)
        self.assertEqual(unicode(group), u'Demo Group (Demo Student)')


class JournalModelTests(TestCase):
    """Test journal model"""

    def test_unicode(self):
        from datetime import date
        student = Student(first_name='Demo', last_name='Student')
        journal = MonthJournal(student=student, date=date(2016, 5, 1))
        self.assertEqual(unicode(journal), u'Student: 5 2016')


class EventModelTests(TestCase):
    """Test event model"""

    def test_unicode(self):
        log_event = LogEntry(evt_type='C', evt_user='Test User', evt_desc='Test Event')
        self.assertIn('Test Event', unicode(log_event))


class StProfileModelTests(TestCase):
    """Test event model"""

    def test_unicode(self):
        user = User(username='user1', email='test@test.com')
        st_user = StProfile(user=user, mobile_phone='355-355')
        self.assertEqual(unicode(st_user), u'user1')
