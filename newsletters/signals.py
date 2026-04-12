from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Subscriber


@receiver(post_save, sender=Subscriber)
def subscriber_created(sender, instance, created, **kwargs):
    if created:
        print(f"New subscriber: {instance.email}")

        # Example: send welcome email (async recommended)
        # send_welcome_email.delay(instance.email)


@receiver(post_save, sender=Subscriber)
def subscriber_status_changed(sender, instance, created, **kwargs):
    if not created:
        if not instance.is_active:
            print(f"Unsubscribed: {instance.email}")
        else:
            print(f"Re-subscribed: {instance.email}")

