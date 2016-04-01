# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student


# Views for Students

def students_list(request):
    students = Student.objects.all()

    # try to order students list

    order_by = request.GET.get('order_by', '')
    if order_by not in ('id', 'first_name', 'ticket'):
        order_by = 'last_name'
    students = students.order_by(order_by)

    reverse_by = request.GET.get('reverse', '')
    if reverse_by == '1':
        students = students.reverse()

    # paginate students
    # PageNotAnInteger: if page is not an integer, deliver first page
    # if page is out of range (e.g. 9999), deliver last page of results
    paginator = Paginator(students, 3)
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students, 'order_by': order_by, 'reverse': reverse_by})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return render(request, 'students/students_edit.html', {})


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
