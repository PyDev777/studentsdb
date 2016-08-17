from django import template
from django.template.loader import get_template


register = template.Library()


# Usage: {% pagenav students is_paginated paginator %}


@register.tag
def pagenav(parser, token):
    # parse tag arguments
    try:
        # split_contents knows how to split quoted strings
        tag_name, object_list, base_url, order_by, reverse, cur_month, is_paginated, paginator = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 7 arguments' % token.contents.split()[0])
    # create PageNavNode object passing tag arguments
    return PageNavNode(object_list, base_url, order_by, reverse, cur_month, is_paginated, paginator)


class PageNavNode(template.Node):
    def __init__(self, object_list, base_url, order_by, reverse, cur_month, is_paginated, paginator):
        self.object_list = template.Variable(object_list)
        self.base_url = template.Variable(base_url)
        self.order_by = template.Variable(order_by)
        self.reverse = template.Variable(reverse)
        self.cur_month = template.Variable(cur_month)
        self.is_paginated = template.Variable(is_paginated)
        self.paginator = template.Variable(paginator)

    def render(self, context):
        t = get_template('students/pagination.html')
        return t.render(template.Context({
            'object_list': self.object_list.resolve(context),
            'base_url': self.base_url.resolve(context),
            'order_by': self.order_by.resolve(context),
            'reverse': self.reverse.resolve(context),
            'cur_month': self.cur_month.resolve(context),
            'is_paginated': self.is_paginated.resolve(context),
            'paginator': self.paginator.resolve(context)
        }, ))
