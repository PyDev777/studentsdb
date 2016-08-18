from django import template
from django.template.loader import get_template


register = template.Library()


# Usage: {% pagenav object_list=students base_url=students_url order_by=order_by reverse=reverse cur_month=cur_month is_paginated=is_paginated paginator=paginator %}

@register.simple_tag
def pagenav(*args, **kwargs):
    t = get_template('students/pagination.html')
    return t.render(template.Context({
        'object_list': kwargs['object_list'],
        'base_url': kwargs['base_url'],
        'order_by': kwargs['order_by'],
        'reverse': kwargs['reverse'],
        'cur_month': kwargs['cur_month'],
        'is_paginated': kwargs['is_paginated'],
        'paginator': kwargs['paginator']}))
