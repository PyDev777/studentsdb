from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Student


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    print sender
