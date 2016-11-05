# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class StProfile(models.Model):
    """To keep extra user data"""
    # user mapping
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = _(u"User Profile")

    # extra user data

    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_(u"Birthday"))

    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name=_(u"Photo"))

    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        default='',
        verbose_name=_(u"Mobile phone"))

    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='',
        verbose_name=_(u"Address"))

    def __unicode__(self):
        return self.user.username
