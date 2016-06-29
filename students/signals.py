# coding: utf-8

import logging
from django.db.models.signals import post_save, post_delete
from django.core.signals import request_started
from django.dispatch import receiver
from .models import Student, Group

req_counter = 0


@receiver(request_started)
def log_request_started(sender, **kwargs):
    """Writes information about the amount of requests into log file"""
    global req_counter
    logger = logging.getLogger(__name__)
    req_counter += 1
    logger.info("Request counter: %d", req_counter)


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student into log file"""
    logger = logging.getLogger(__name__)
    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
    else:
        logger.info("Student updated: %s %s (ID: %d)", student.first_name, student.last_name, student.id)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about newly deleted student into log file"""
    logger = logging.getLogger(__name__)
    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)", student.first_name, student.last_name, student.id)


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated group into log file"""
    logger = logging.getLogger(__name__)
    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group added: %s (ID: %d)", group.title, group.id)
    else:
        logger.info("Group updated: %s (ID: %d)", group.title, group.id)


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about newly deleted group into log file"""
    logger = logging.getLogger(__name__)
    group = kwargs['instance']
    logger.info("Group deleted: %s (ID: %d)", group.title, group.id)
