from django import template

register = template.Library()


@register.filter
def str2int(string):
    """Convert input string into integer. If can not convert, return 0"""
    try:
        value = int(string)
    except ValueError:
        value = 0
    return value
