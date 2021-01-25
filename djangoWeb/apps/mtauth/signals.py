from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from .models import MTUser


@receiver([post_save], sender=MTUser)
def send_register_email(*args, **kwargs):
    print('111111111111111')
