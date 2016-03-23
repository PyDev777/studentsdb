# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# Create your views here.

# Views for Students

def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Андрій',
         'last_name': u'Корост',
         'ticket': 2123,
         'image': 'img/podoba3.jpg'},
        {'id': 2,
         'first_name': u'Віталій',
         'last_name': u'Подоба',
         'ticket': 254,
         'image': 'img/me.jpeg'},
        {'id': 3,
         'first_name': u'Тарас',
         'last_name': u'Притула',
         'ticket': 5332,
         'image': 'img/piv.png'}
    )
    return render(request, 'students/students_list.html', {'students': students, 'students_url': reverse('home')})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return render(request, 'students/students_edit.html', {})

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


# Views for Groups

def groups_list(request):
    groups = (
        {"id": 1,
         "name": u'МтМ-21',
         "leader": {"id": 1, "name": u'Ячменев Олег'}},
        {"id": 2,
         "name": u'МтМ-22',
         "leader": {"id": 2, "name": u'Подоба Віталій'}},
        {"id": 3,
         "name": u'МтМ-23',
         "leader": {"id": 3, "name": u'Іванов Андрій'}}
    )
    return render(request, 'students/groups_list.html', {'groups': groups, 'groups_url': reverse('groups')})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


# Views for Journal

def journal(request):
    return render(request, 'students/journal.html', {'journal_url': reverse('journal')})

