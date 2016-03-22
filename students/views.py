# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader


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
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


# Views for Groups

def groups_list(request):
    groups = (
        {"id": 1,
         "group_name": 'МтМ-21',
         "group_leader": 'Ячменев Олег'},
        {"id": 2,
         "group_name": 'МтМ-22',
         "group_leader": 'Подоба Віталій'},
        {"id": 3,
         "group_name": 'МтМ-23',
         "group_leader": 'Іванов Андрій'}
    )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


