from django.conf.urls import patterns, include, url
from django.contrib import admin
from students.views.students import StudentAddView, StudentUpdateView, StudentDeleteView, StudentListView
from students.views.groups import GroupAddView, GroupUpdateView, GroupDeleteView, GroupListView
from students.views.events_log import EventLogView
from students.views.contact_admin import ContactAdminView, ContactLetterView
from students.views.journal import JournalView
from .settings import MEDIA_ROOT, DEBUG

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentsdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Students urls
    url(r'^$', StudentListView.as_view(), name='home'),
    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', GroupListView.as_view(), name='groups'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

    # Journal
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Events
    url(r'^events_log/$', EventLogView.as_view(), name='events_log'),

    # Contact Admin Form
    url(r'^contact-admin/$', ContactAdminView.as_view(), name='contact_admin'),
    url(r'^contact-letter/$', ContactLetterView.as_view(), name='contact_letter'),


    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
