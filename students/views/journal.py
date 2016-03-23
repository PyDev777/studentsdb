# coding: utf-8

from django.shortcuts import render
from django.core.urlresolvers import reverse


# Views for Journal

def journal(request):
    return render(request, 'students/journal.html', {'journal_url': reverse('journal')})

