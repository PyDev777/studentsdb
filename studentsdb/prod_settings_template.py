##############################################
#                                            #
#  Rename this file to prod_settings.py and  #
#  enter your values to his settings fields  #
#                                            #
##############################################

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '================= Your SECRET_KEY ================'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'domain_name']


# DATABASES settings
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# MySQL settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'students_db_user',
        'PASSWORD': 'students_db_user_password',
        'NAME': 'students_db',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'students', 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

# Template files
TEMPLATE_DEBUG = False
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'studentsdb', 'templates'),
                 os.path.join(BASE_DIR, 'stud_auth', 'templates'),
                 os.path.join(BASE_DIR, 'students', 'templates', 'students'), )


# Social settings
SOCIAL_AUTH_FACEBOOK_KEY = '=== Your pub key ==='
SOCIAL_AUTH_FACEBOOK_SECRET = '=== Your sec key ==='


# Admins
ADMINS = (('John', 'john@example.com'),)
MANAGERS = (('Peter', 'peter@example.com'),)

# EMAIL settings (use SSL)
ADMIN_EMAIL = 'john@example.com'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'sender@example.com'
EMAIL_HOST_PASSWORD = 'sender_password'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SERVER_EMAIL = 'sender@example.com'
DEFAULT_FROM_EMAIL = 'sender@example.com'


# Logging settings
LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'students.signals': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO'
        },
        'registration.signals': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO'
        },
        'students.views.contact_admin': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO'
        }
    }
}
