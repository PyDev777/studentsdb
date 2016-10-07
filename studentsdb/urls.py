from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import RedirectView, TemplateView
from registration.backends.default.views import RegistrationView as rRegView, ActivationView as rActView
from registration.forms import RegistrationFormUniqueEmail as rFormUniqueEmail
from students.views.students import StudentAddView, StudentUpdateView, StudentDeleteView, StudentListView
from students.views.groups import GroupAddView, GroupUpdateView, GroupDeleteView, GroupListView
from students.views.events_log import EventLogView
from students.views.contact_admin import ContactAdminView, ContactLetterView
from students.views.journal import JournalView


###################################################
#                                                 #
#                   WARNING!                      #
#                                                 #
#      Read instruction bottom of this file       #
#                                                 #
###################################################


js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',

    # Social Auth Related urls
    url('^social/', include('social.apps.django_app.urls', namespace='social')),


    # User Related urls
    url(r'^users/register/$', rRegView.as_view(form_class=rFormUniqueEmail), name='registration_register'),
    # url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    # url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), kwargs={'next_page': 'home'}, name='registration_complete'),

    # url(r'^users/activate/(?P<activation_key>\w+)/$', rActView.as_view(), name='registration_activate'),
    url(r'^activate/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_activation_complete'),

    url(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),

    url(r'^users/logout/$', auth_view.logout, kwargs={'next_page': 'home'}, name='auth_logout'),

    url(r'^users/', include('registration.backends.default.urls', namespace='users')),
    # url(r'^users/', include('registration.backends.simple.urls', namespace='users')),


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
    url(r'^contact-admin/$', permission_required('auth.add_user')(ContactAdminView.as_view()), name='contact_admin'),
    url(r'^contact-letter/$', permission_required('auth.add_user')(ContactLetterView.as_view()), name='contact_letter'),

    # Captcha
    url(r'^captcha/', include('captcha.urls')),

    # JS i18n
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)


###################################################
#                                                 #
#                   WARNING!                      #
#                                                 #
#  This code block only for development mode and  #
#  testing NON REAL production mode!              #
#                                                 #
#  Comment or delete this code block for REAL     #
#  production mode!                               #
#                                                 #
###################################################
#                                                 #
#                                                 #
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
else:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
    urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))
#                                                 #
###################################################
