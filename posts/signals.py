from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from .models import Like, Comment


# ==========================
# 🔥 LIKE SIGNALS
# ==========================

@receiver(post_save, sender=Like)
def increase_like_count(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.likes_count = F('likes_count') + 1
        post.save(update_fields=['likes_count'])


@receiver(post_delete, sender=Like)
def decrease_like_count(sender, instance, **kwargs):
    post = instance.post
    post.likes_count = F('likes_count') - 1
    post.save(update_fields=['likes_count'])


# ==========================
# 🔥 COMMENT SIGNALS
# ==========================

@receiver(post_save, sender=Comment)
def increase_comment_count(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comments_count = F('comments_count') + 1
        post.save(update_fields=['comments_count'])


@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = F('comments_count') - 1
    post.save(update_fields=['comments_count'])