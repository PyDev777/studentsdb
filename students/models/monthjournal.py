# coding: utf-8

from django.db import models


class MonthJournal(models.Model):
    """Student Mounth Journal """

    class Meta:
        verbose_name = u'Місячний журнал'
        verbose_name_plural = u'Місячні Журнали'

    student = models.ForeignKey(
        'Student',
        verbose_name=u'Студент',
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name=u'Дата',
        blank=False)

    def __unicode__(self):
        return u'%s: %d %d' % (self.student.last_name, self.date.month, self.date.year)


for i in range(1, 32):
    MonthJournal.add_to_class('present_day%s' % i, models.BooleanField(default=False))
