from django.db import models
from django.conf import settings


class Follow(models.Model):
    FOLLOW_TYPE_CHOICES = (
        ('user', 'User'),
        ('company', 'Company'),
    )

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers'
    )
    follow_type = models.CharField(max_length=20, choices=FOLLOW_TYPE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]

    def __str__(self):
        return f"{self.follower.email} follows {self.following.email}"
