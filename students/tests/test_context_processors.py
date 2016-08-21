from django.test import TestCase
from django.http import HttpRequest

from students.context_processors import groups_processor


class ContextProcessorsTests(TestCase):

    fixtures = ['students_test_data.json']

    def test_groups_processor(self):
        """Test groups processor"""
        request = HttpRequest()
        data = groups_processor(request)

        # test data from processor
        self.assertEqual(len(data['GROUPS']), 2)
        self.assertEqual(data['GROUPS'][0]['title'], u'Group1')
        self.assertEqual(data['GROUPS'][1]['title'], u'Group2')
