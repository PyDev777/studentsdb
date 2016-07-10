# coding: utf-8

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = _(u'Students Database')

    def ready(self):
        from students import signals
