############################################
#                                          #
#  Rename this file to local_settings.py   #
#                                          #
############################################

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '================= Your SECRET_KEY ================'

# PORTAL settings
PORTAL_PROTOCOL = 'http'
PORTAL_DOMAIN = '127.0.0.1'
PORTAL_PORT = '8000'

# DATABASES settings (use SQLite)
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}

# EMAIL settings (use SSL)
ADMINS = [('John', 'john@example.com')]
ADMIN_EMAIL = 'john@example.com'
SERVER_EMAIL = 'sender@example.com'
DEFAULT_FROM_EMAIL = 'sender@example.com'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'sender@example.com'
EMAIL_HOST_PASSWORD = 'sender_password'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


