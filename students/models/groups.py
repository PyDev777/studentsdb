# coding: utf-8

from django.db import models


# Create your models here.

class Group(models.Model):
    """Group model"""

    class Meta(object):
        verbose_name = u'Група'
        verbose_name_plural = u'Групи'

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва")

    leader = models.OneToOneField(
        'Student',
        null=True,
        blank=True,
        verbose_name=u"Староста",
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % self.title
