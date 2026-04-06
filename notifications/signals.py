from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from notifications.models import Notification

User = get_user_model()


def create_notification(recipient, notification_type, message, sender=None, **kwargs):
    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        message=message,
        title=kwargs.get('title', ''),
        action_url=kwargs.get('action_url', ''),
        related_object_id=kwargs.get('related_object_id')
    )


# Example integrations (plug into your other models)

@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        create_notification(
            recipient=instance,
            notification_type='system',
            message="Welcome to the platform!",
            title="Welcome 🎉"
        )


# Example: from Connection model
@receiver(post_save, sender='your_app.Connection')
def connection_notification(sender, instance, created, **kwargs):
    if created:
        create_notification(
            recipient=instance.receiver,
            sender=instance.sender,
            notification_type='connection_request',
            message="You have a new connection request",
            related_object_id=instance.id
        )
    elif instance.status == 'accepted':
        create_notification(
            recipient=instance.sender,
            sender=instance.receiver,
            notification_type='connection_accepted',
            message="Your connection request was accepted",
            related_object_id=instance.id
        )


# Example: from Message model
@receiver(post_save, sender='your_app.Message')
def message_notification(sender, instance, created, **kwargs):
    if created:
        create_notification(
            recipient=instance.receiver,
            sender=instance.sender,
            notification_type='message',
            message="You received a new message",
            related_object_id=instance.id
        )