# coding: utf-8

import logging
from django.db.models.signals import post_save, post_delete
from django.core.signals import request_started
from django.dispatch import receiver
from .models import Student, Group, LogEntry

req_counter = 0


@receiver(request_started)
def log_request_started(sender, **kwargs):
    """Writes information about the amount of requests into log file"""

    global req_counter
    req_counter += 1

    logger = logging.getLogger(__name__)
    logger.info("Requests counter: %s" % req_counter)


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student into log file"""

    student = kwargs['instance']
    msg = "Student %s: %s (ID: %d)" % ("added" if kwargs['created'] else "updated", student, student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about newly deleted student into log file"""

    student = kwargs['instance']
    msg = "Student deleted: %s (ID: %d)" % (student, student.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated group into log file"""

    group = kwargs['instance']
    msg = "Group %s: %s (ID: %d)" % ("added" if kwargs['created'] else "updated", group, group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("C" if kwargs['created'] else "U", msg)


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about newly deleted group into log file"""

    group = kwargs['instance']
    msg = "Group deleted: %s (ID: %d)" % (group, group.id)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    saveLogEntry("D", msg)


def saveLogEntry(e_type, e_desc):
    ev = LogEntry()
    ev.evt_type = e_type
    ev.evt_user = 'Anonimus'
    ev.evt_description = e_desc
    ev.save()
