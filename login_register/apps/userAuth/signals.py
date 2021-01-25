from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile
from .utils import send_email


@receiver(post_save, sender=UserProfile)
def email_active(instance, created, **kwargs):
    if created:
        email = instance.email
        active_code = instance.active_code
        send_email(email, active_code)
        # print('发邮件')
