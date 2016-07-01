# coding: utf-8

from django.db import models

# Create your models here.


class LogEntry(models.Model):
    """LogEntry model"""

    class Meta(object):
        verbose_name = u'Подія'
        verbose_name_plural = u'Події'

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Час створення')

    # C - create, U - update, D - delete
    evt_type = models.CharField(
        max_length=1,
        verbose_name=u'Тип події')

    evt_user = models.CharField(
        max_length=30,
        verbose_name=u'Користувач')

    evt_description = models.CharField(
        max_length=200,
        verbose_name=u'Опис події')

    def __unicode__(self):
        return u"%s %s" % (self.timestamp, self.evt_description)
