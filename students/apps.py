# coding: utf-8

from django.apps import AppConfig


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = u'База Студентів'

    def ready(self):
        from students import signals
