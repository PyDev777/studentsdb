from django import template

register = template.Library()


# Usage: {% pagenav object_list=students base_url=students_url order_by=order_by reverse=reverse cur_month=cur_month is_paginated=is_paginated paginator=paginator %}

@register.inclusion_tag('students/pagination.html')
def pagenav(object_list, base_url, order_by, reverse, cur_month, is_paginated, paginator):
    """Display page navigation for given list of objects"""
    return {'object_list': object_list,
            'base_url': base_url,
            'order_by': order_by,
            'reverse': reverse,
            'cur_month': cur_month,
            'is_paginated': is_paginated,
            'paginator': paginator}
