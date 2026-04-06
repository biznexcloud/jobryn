from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Follow


@receiver(post_save, sender=Follow)
def follow_created(sender, instance, created, **kwargs):
    if created:
        # Example: increment followers count (if you have field)
        follower = instance.follower
        following = instance.following

        # Optional logic
        print(f"{follower.email} started following {following.email}")

        # Example (if profile model exists):
        # following.profile.followers_count += 1
        # following.profile.save()


@receiver(post_delete, sender=Follow)
def follow_deleted(sender, instance, **kwargs):
    follower = instance.follower
    following = instance.following

    print(f"{follower.email} unfollowed {following.email}")

    # Example:
    # following.profile.followers_count -= 1
    # following.profile.save()