# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from ..models import Student


# Views for Students

def students_list(request):
    students = Student.objects.all()
    return render(request, 'students/students_list.html', {'students': students, 'students_url': reverse('home')})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return render(request, 'students/students_edit.html', {})


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
