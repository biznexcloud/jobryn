from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Connection


@receiver(post_save, sender=Connection)
def connection_created(sender, instance, created, **kwargs):
    if created:
        print(f"Connection request sent from {instance.sender.email} to {instance.receiver.email}")

        # Example: trigger notification
        # send_notification(instance.receiver, "New connection request")


@receiver(post_save, sender=Connection)
def connection_status_updated(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'accepted':
            print(f"{instance.receiver.email} accepted connection from {instance.sender.email}")

            # Example:
            # instance.sender.profile.connections_count += 1
            # instance.receiver.profile.connections_count += 1
            # instance.sender.profile.save()
            # instance.receiver.profile.save()

        elif instance.status == 'declined':
            print(f"{instance.receiver.email} declined connection")

        elif instance.status == 'blocked':
            print(f"{instance.receiver.email} blocked {instance.sender.email}")


@receiver(post_delete, sender=Connection)
def connection_deleted(sender, instance, **kwargs):
    print(f"Connection removed between {instance.sender.email} and {instance.receiver.email}")