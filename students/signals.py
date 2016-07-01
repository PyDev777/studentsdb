# coding: utf-8

import logging
from django.db.models.signals import post_save, post_delete, post_migrate
from django.core.signals import request_started
from django.dispatch import receiver, Signal
from .models import Student, Group, LogEntry

req_counter = 0
contact_letter_sent = Signal()


@receiver(request_started)
def log_request_started(sender, **kwargs):
    """Writes information about the amount of requests into log file"""

    global req_counter
    req_counter += 1

    logger = logging.getLogger(__name__)
    logger.info(u"Кількість запитів: %s" % req_counter)


@receiver(contact_letter_sent)
def log_contact_admin(sender, **kwargs):
    """Writes information about contact letter sent into log file"""

    logger = logging.getLogger(__name__)
    logger.info(u"Надіслано повідомлення від %s" % kwargs['email'])


@receiver(post_migrate)
def log_migrate_event(sender, **kwargs):
    """Writes information about migrate into log file"""

    if kwargs['app_config'].label == 'students':
        msg = u"Міграцію бази даних виконано"

        logger = logging.getLogger(__name__)
        logger.info(msg)

        saveLogEntry("M", msg)


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student into log file"""

    student = kwargs['instance']
    msg = u"Студента %s %s (ID: %d)" % (student, u"додано" if kwargs['created'] else u"оновлено", student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about newly deleted student into log file"""

    student = kwargs['instance']
    msg = u"Студента %s видалено (ID: %d)" % (student, student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated group into log file"""

    group = kwargs['instance']
    msg = u"Групу %s %s (ID: %d)" % (group, u"додано" if kwargs['created'] else u"оновлено", group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about newly deleted group into log file"""

    group = kwargs['instance']
    msg = u"Групу %s видалено (ID: %d)" % (group, group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


def saveLogEntry(e_type, e_desc):
    ev = LogEntry()
    ev.evt_type = e_type
    ev.evt_user = 'Anonimus'
    ev.evt_desc = e_desc
    ev.save()
