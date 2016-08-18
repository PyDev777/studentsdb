from django import template

register = template.Library()


@register.filter
def nice_username(user):
    """
    Return nice username for logged user.
    Is user.get_full_name() present - return it, else user.username.
    If user is superuser: *** nice_username ***.
    If user is staff and not superuser: * nice_username *.
    """
    rank = '***' if user.is_superuser else '*' if user.is_staff and not user.is_superuser else ''
    return rank + ' ' + (user.get_full_name() or user.username) + ' ' + rank
