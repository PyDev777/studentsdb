from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects, per_page, request, context, var_name='object_list'):
    """Paginate objects provided by view.
    This function takes:
    * objects - list of elements;
    * per_page - number of objects per page;
    * request object to get url parameters from;
    * context to set new variables into;
    * var_name - variable name for list of objects.
    It returns updated context object.
    """

    # apply pagination
    paginator = Paginator(objects, per_page)
    # try to get page number from request
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        object_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        object_list = paginator.page(paginator.num_pages)

    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context


def get_current_group(request):
    """Returns currently selected group or None"""

    # we remember selected group in a cookie
    pk = request.COOKIES.get('current_group')
    if pk:
        from .models import Group
        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None


def get_groups(request):
    """Returns list of existing groups"""

    from .models import Group

    # get currently selected group
    cur_group = get_current_group(request)

    groups = []
    for group in Group.objects.all().order_by('title'):
        groups.append({
            'id': group.id,
            'title': group.title,
            'leader': group.leader and (u'%s %s' % (group.leader.first_name, group.leader.last_name)) or None,
            'selected': cur_group and cur_group.id == group.id and True or False
        })

    return groups
