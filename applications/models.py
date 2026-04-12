from django.db import models
from django.conf import settings
from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('online_meeting', 'Online Meeting'),
        ('onsite_meeting', 'On-site Meeting'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    feedback_for_seeker = models.TextField(blank=True)

    # 👨‍💼 RECRUITER TOOLS
    interview_score = models.PositiveSmallIntegerField(null=True, blank=True)  # 1–100
    internal_notes = models.TextField(blank=True)

    # 💰 HIRE INFO (Snapshot at time of hiring)
    accepted_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_type = models.CharField(max_length=20, blank=True)  # mirror from Job at hire time
    hired_at = models.DateTimeField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    payroll_initialized = models.BooleanField(default=False)
    commission_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'seeker')
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['seeker', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.seeker.email} → {self.job.title} [{self.status}]"
