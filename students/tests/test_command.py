from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
import os
from django.contrib.auth.models import User
from students.models import Student, Group


class FillDBTest(TestCase):
    """Test fill_db command"""

    fixtures = ['students_test_data.json']

    def test_success(self):

        students_count_before = len(Student.objects.all())
        groups_count_before = len(Group.objects.all())
        users_count_before = len(User.objects.all())

        # prepare output file for command
        out = StringIO()

        # call our command
        call_command('fill_db', student=5, group=4, user=3, stdout=out)

        students_count_after = len(Student.objects.all())
        groups_count_after = len(Group.objects.all())
        users_count_after = len(User.objects.all())

        # get command output
        result = out.getvalue()

        # check if we get proper number of objects in database
        self.assertEqual(students_count_before + 5, students_count_after)
        self.assertEqual(groups_count_before + 4, groups_count_after)
        self.assertEqual(users_count_before + 3, users_count_after)

        self.assertNotIn('ERROR!', result)
        self.assertIn('created successfully', result)


class STCountTest(TestCase):
    """Test stcount command"""

    fixtures = ['students_test_data.json']

    def test_command_output(self):
        # prepare output file for command
        out = StringIO()

        # call our command
        call_command('stcount', 'student', 'group', 'user', stdout=out)

        # get command output
        result = out.getvalue()

        # check if we get proper number of objects in database
        self.assertIn('students in database: 4', result)
        self.assertIn('groups in database: 3', result)
        self.assertIn('users in database: 3', result)


class LocalizeStaticTest(TestCase):
    """Test localize_static command"""

    def test_localize(self):

        template = 'students/templates/students/base.html'

        try:
            with open(template, 'r') as f:
                t = f.read()
        except IOError as e:
            print 'ERROR!\n%s\nBase template not modified.' % e.message
            raise SystemExit(1)

        try:
            os.rename(template, template + '.bak')
        except IOError as e:
            print 'ERROR!\n%s\nBase template not modified.' % e.message
            raise SystemExit(1)

        try:
            with open(template, 'w') as f:
                f.write(t)
        except IOError as e:
            print 'ERROR!\n%s\nOriginal base template is base.html.bak.' % e.message
            raise SystemExit(1)

        # prepare output file for command
        out = StringIO()
        # call command to localize_static (check status)
        call_command('localize_static', stdout=out)
        # get command output
        result = out.getvalue()
        self.assertNotIn('ERROR!', result)
        self.assertIn('Localized static status', result)

        if 'online' in result:
            self.assertIn('online', result)

            # call command to localize_static to online (again)
            out = StringIO()
            call_command('localize_static', '--online', ls=False, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('No commented CDN tags.\nLocalized static status: online', result)

            # call command to localize_static to offline
            out = StringIO()
            call_command('localize_static', '--offline', ls=True, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('Download file:', result)
            self.assertIn('OK', result)
            self.assertIn('Localized static status: offline', result)

            # call command to localize_static to offline (again)
            out = StringIO()
            call_command('localize_static', '--offline', ls=True, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('No CDN tags.\nLocalized static status: offline', result)

            # call command to localize_static to online
            out = StringIO()
            call_command('localize_static', '--online', ls=False, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('Localized static status: online', result)
        else:
            self.assertIn('offline', result)

            # call command to localize_static to offline (again)
            out = StringIO()
            call_command('localize_static', '--offline', ls=True, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('No CDN tags.\nLocalized static status: offline', result)

            # call command to localize_static to online
            out = StringIO()
            call_command('localize_static', '--online', ls=False, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('Localized static status: online', result)

            # call command to localize_static to online (again)
            out = StringIO()
            call_command('localize_static', '--online', ls=False, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('No commented CDN tags.\nLocalized static status: online', result)

            # call command to localize_static to offline
            out = StringIO()
            call_command('localize_static', '--offline', ls=True, stdout=out)
            result = out.getvalue()
            self.assertNotIn('ERROR!', result)
            self.assertIn('Download file:', result)
            self.assertIn('OK', result)
            self.assertIn('Localized static status: offline', result)

        try:
            os.remove(template)
        except IOError as e:
            print 'ERROR!\n%s\nOriginal base template is base.html.bak.' % e.message
            raise SystemExit(1)

        try:
            os.rename(template + '.bak', template)
        except IOError as e:
            print 'ERROR!\n%s\nOriginal base template is base.html.bak.' % e.message
            raise SystemExit(1)
