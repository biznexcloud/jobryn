from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('message', 'New Message'),
        ('job_application', 'Job Application'),
        ('application_update', 'Application Status Update'),
        ('post_like', 'Post Liked'),
        ('post_comment', 'Post Commented'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('meeting_updated', 'Meeting Updated'),
        ('course_enrolled', 'Course Enrolled'),
        ('system', 'System Alert'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    action_url = models.CharField(max_length=500, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.notification_type}] → {self.recipient.email}"
