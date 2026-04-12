from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Stori(models.Model):
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('connections', 'Connections'),
        ('private', 'Only Me'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )

    caption = models.TextField(blank=True)
    images = models.ImageField(upload_to='story_images/')

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='public'
    )

    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Story by {self.author.email}"
   
class StoriView(models.Model):
    story = models.ForeignKey(
        Stori,
        on_delete=models.CASCADE,
        related_name='views'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')
        indexes = [
            models.Index(fields=['story']),
        ]
class StoriLike(models.Model):
    story = models.ForeignKey(
        Stori,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')
        indexes = [
            models.Index(fields=['story']),
        ]

    def __str__(self):
        return f"{self.user.email} liked Story {self.story.id}"
    
class StoriComment(models.Model):
    story = models.ForeignKey(
        Stori,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.email}"
    
class StoriTag(models.Model):
    story = models.ForeignKey(
        Stori,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    tagged_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tagged_in_stories'
    )

    tagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tagged_users_in_stories'
    )

    # Optional positioning (for UI like Instagram)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'tagged_user')
        indexes = [
            models.Index(fields=['story']),
        ]
