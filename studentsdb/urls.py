from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import RedirectView, TemplateView
from registration.backends.default.views import RegistrationView, ActivationView
from stud_auth.forms import CustomRegistrationFormUniqueEmail, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm
from stud_auth.views import custom_password_reset_confirm, custom_activation_complete
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

# def ajaxRequest(request):
#     return request.is_ajax()
#
# info_dict = {
#     'req': ajaxRequest(),
# }

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Social Auth Related urls
    url('^social/', include('social.apps.django_app.urls', namespace='social')),

    # User Related urls
    url(r'^users/register/$', RegistrationView.as_view(form_class=CustomRegistrationFormUniqueEmail), name='registration_register'),
    url(r'^users/register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^users/register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'), name='registration_disallowed'),
    url(r'^users/activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^users/activate/complete/$', custom_activation_complete, name='registration_activation_complete'),
    # url(r'^users/activate/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_activation_complete'),
    url(r'^users/login/$', auth_view.login, {'authentication_form': CustomAuthenticationForm}, name='auth_login'),
    url(r'^users/logout/$', auth_view.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^users/password_reset/$', auth_view.password_reset, {'password_reset_form': CustomPasswordResetForm}, name='password_reset'),
    url(r'^users/password_reset/done/$', auth_view.password_reset_done, name='password_reset_done'),
    url(r'^users/password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', custom_password_reset_confirm, name='password_reset_confirm'),
    url(r'^users/password_reset/complete/$', auth_view.password_reset_complete, name='password_reset_complete'),
    url(r'^users/password_change/$', auth_view.password_change, {'password_change_form': CustomPasswordChangeForm}, name='password_change'),
    url(r'^users/password_change/done/$', auth_view.password_change_done, name='password_change_done'),
    url(r'^users/', include('registration.backends.default.urls', namespace='users')),

    # User profile
    url(r'^profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),

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

    # Events log
    url(r'^events_log/$', login_required(EventLogView.as_view()), name='events_log'),

    # Contact Admin Form
    url(r'^contact-admin/$', permission_required('auth.add_user')(ContactAdminView.as_view()), name='contact_admin'),
    url(r'^contact-letter/$', permission_required('auth.add_user')(ContactLetterView.as_view()), name='contact_letter'),

    # Captcha
    url(r'^captcha/', include('captcha.urls')),

    # JS i18n
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),

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
