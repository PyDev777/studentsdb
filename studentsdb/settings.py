"""
Django settings for studentsdb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from django.conf import global_settings


###############################################################################
#                                                                             #
# This setting determines which mode will be used - Development or Production #
#                                                                             #
###############################################################################
#                                                                             #
#                                                                             #
PRODUCTION_MODE = True
#                                                                             #
#                                                                             #
###############################################################################

try:
    if PRODUCTION_MODE:
        from prod_settings import *
    else:
        from dev_settings import *
except ImportError:
    pass


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'registration',
    'social.apps.django_app.default',
    'django_coverage',
    'captcha',
    'students',
    'stud_auth',
)

MIDDLEWARE_CLASSES_TUPLE = (
    'studentsdb.middleware.RequestTimeMiddleware',
    'studentsdb.middleware.DBTimeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES_TUPLE[2:] if PRODUCTION_MODE else MIDDLEWARE_CLASSES_TUPLE


TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "studentsdb.context_processors.students_proc",
    "students.context_processors.groups_processor",
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Crispy forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Registration settings
REGISTRATION_OPEN = True
LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True


# Coverage report settings
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'coverage')


