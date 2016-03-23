# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse


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
