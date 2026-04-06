from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        print(f"New message from {instance.sender.email} to {instance.receiver.email}")

        # Example: trigger notification
        # send_notification(instance.receiver, "New message received")


@receiver(post_save, sender=Message)
def message_read_status(sender, instance, created, **kwargs):
    if not created and instance.is_read:
        print(f"Message read by {instance.receiver.email}")

        # Example:
        # notify sender that message was read