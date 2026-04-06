from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Story, StoryLike, StoryView, StoryComment, StoryMedia


@receiver(post_save, sender=StoryLike)
def increase_story_like(sender, instance, created, **kwargs):
    if created:
        Story.objects.filter(id=instance.story.id).update(
            likes_count=F('likes_count') + 1
        )


@receiver(post_delete, sender=StoryLike)
def decrease_story_like(sender, instance, **kwargs):
    Story.objects.filter(id=instance.story.id).update(
        likes_count=F('likes_count') - 1
    )


@receiver(post_save, sender=StoryView)
def increase_story_view(sender, instance, created, **kwargs):
    if created:
        Story.objects.filter(id=instance.story.id).update(
            views_count=F('views_count') + 1
        )