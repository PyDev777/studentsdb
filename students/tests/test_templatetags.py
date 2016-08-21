from django.template import Template, Context
from django.test import TestCase
from django.core.paginator import Paginator


class TemplateTagTests(TestCase):

    def test_pagenav_tag(self):
        """Pagenav tag returns page navigation widget"""
        # prepare paginator
        paginator = Paginator([1, 2, 3, 4], 1)
        my_list = paginator.page('1')
        test_url = 'test/'

        # render template with pagenav tag
        out = Template(
            "{% load pagenav %}"
            "{% pagenav object_list base_url order_by reverse cur_month is_paginated paginator %}"
        ).render(Context({
            'object_list': my_list, 'base_url': test_url, 'order_by': None, 'reverse': None, 'cur_month': None, 'is_paginated': True, 'paginator': paginator
        }))

        # paginator should create 4 pages
        self.assertIn('<nav>', out)
        self.assertIn('<a href="test/?page=1" class="content-link">1</a>', out)
        self.assertIn('<a href="test/?page=2" class="content-link">2</a>', out)
        self.assertIn('<a href="test/?page=3" class="content-link">3</a>', out)
        self.assertIn('<a href="test/?page=4" class="content-link">4</a>', out)

    def test_str2int(self):
        """Test str2int template filter"""
        out = Template(
            "{% load str2int %}"
            "{% if 36 == '36'|str2int %}"
            "it works"
            "{% endif  %}"
        ).render(Context({}))

        # check for our addition operation result
        self.assertIn("it works", out)
