# coding: utf-8

import logging
from django.db.models.signals import post_save, post_delete, post_migrate
from django.core.signals import request_started
from django.dispatch import receiver, Signal
from students.models import Student, Group, LogEntry
from django.utils.translation import ugettext as _

req_counter = 0
contact_letter_sent = Signal()


@receiver(request_started)
def log_request_started(sender, **kwargs):
    """Writes information about the amount of requests into log file"""

    global req_counter
    req_counter += 1

    logger = logging.getLogger(__name__)
    logger.info(u"%s: %s" % (_(u'Requests count'), req_counter))


@receiver(contact_letter_sent)
def log_contact_admin(sender, **kwargs):
    """Writes information about contact letter sent into log file"""

    logger = logging.getLogger(__name__)
    logger.info(u"%s %s" % (_(u'Sent a message from'), kwargs['email']))


@receiver(post_migrate)
def log_migrate_event(sender, **kwargs):
    """Writes information about migrate into log file"""

    if kwargs['app_config'].label == 'students':
        msg = _(u'Database migration completed')

        logger = logging.getLogger(__name__)
        logger.info(msg)

        saveLogEntry("M", msg)


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student into log file"""

    student = kwargs['instance']
    msg = u"%s %s %s (ID: %d)" % (_(u'Student'), student, _(u'added') if kwargs['created'] else _(u'updated'), student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about newly deleted student into log file"""

    student = kwargs['instance']
    msg = u"%s %s %s (ID: %d)" % (_(u'Student'), student, _(u'deleted'), student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated group into log file"""

    group = kwargs['instance']
    msg = u"%s %s %s (ID: %d)" % (_(u'Group'), group, _(u'added') if kwargs['created'] else _(u'updated'), group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about newly deleted group into log file"""

    group = kwargs['instance']
    msg = u"%s %s %s (ID: %d)" % (_(u'Group'), group, _(u'deleted'), group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


def saveLogEntry(e_type, e_desc):
    ev = LogEntry()
    ev.evt_type = e_type
    ev.evt_user = 'Anonimus'
    ev.evt_desc = e_desc
    ev.save()
