# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Group(models.Model):
    """Group model"""

    class Meta(object):
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Title"))

    leader = models.OneToOneField(
        'Student',
        null=True,
        blank=True,
        verbose_name=_(u"Leader"),
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Extra Notes"))

    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % self.title
