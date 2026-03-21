from django.db import models
from django.conf import settings
from applications.models import Application


class Meeting(models.Model):
    MEETING_TYPE_CHOICES = (
        ('online', 'Online Meeting'),
        ('onsite', 'On-site Meeting'),
        ('phone', 'Phone Call'),
    )

    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='meetings')
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='conducted_meetings'
    )
    meeting_type = models.CharField(max_length=10, choices=MEETING_TYPE_CHOICES)
    scheduled_at = models.DateTimeField()
    meeting_link = models.URLField(null=True, blank=True)       # For online meetings
    location_address = models.TextField(null=True, blank=True)  # For on-site meetings
    duration_minutes = models.PositiveIntegerField(default=30)
    recording_url = models.URLField(null=True, blank=True)
    agenda = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    candidate_no_show = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'
        indexes = [
            models.Index(fields=['application', 'status']),
            models.Index(fields=['scheduled_at']),
        ]

    def __str__(self):
        return f"{self.get_meeting_type_display()} — {self.application.seeker.email} [{self.status}]"
