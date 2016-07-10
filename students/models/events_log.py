# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class LogEntry(models.Model):
    """LogEntry model"""

    class Meta(object):
        verbose_name = _(u"Event")
        verbose_name_plural = _(u"Events")

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u"Create time"))

    # C - create, U - update, D - delete, M - migrate
    evt_type = models.CharField(
        max_length=1,
        verbose_name=_(u"Event type"))

    evt_user = models.CharField(
        max_length=30,
        verbose_name=_(u"User"))

    evt_desc = models.CharField(
        max_length=180,
        verbose_name=_(u"Event description"))

    def __unicode__(self):
        return u"%s %s" % (self.timestamp, self.evt_desc)
