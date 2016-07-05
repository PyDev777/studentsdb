from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
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

    # User Related urls
    url(r'^users/logout/$', auth_view.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # Students urls
    url(r'^$', StudentListView.as_view(), name='home'),
    url(r'^students/add/$', login_required(StudentAddView.as_view()), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', login_required(StudentUpdateView.as_view()), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', login_required(StudentDeleteView.as_view()), name='students_delete'),

    # Groups urls
    url(r'^groups/$', login_required(GroupListView.as_view()), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', login_required(GroupDeleteView.as_view()), name='groups_delete'),

    # Journal
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),

    # Events
    url(r'^events_log/$', login_required(EventLogView.as_view()), name='events_log'),

    # Contact Admin Form
    url(r'^contact-admin/$', login_required(ContactAdminView.as_view()), name='contact_admin'),
    url(r'^contact-letter/$', login_required(ContactLetterView.as_view()), name='contact_letter'),

    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
