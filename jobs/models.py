from django.db import models
from django.conf import settings


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    )

    PAYMENT_CHOICES = (
        ('fixed', 'Fixed Price'),
        ('payroll', 'Monthly Payroll'),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead / Principal'),
        ('executive', 'Executive'),
    )

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs'
    )
    company = models.ForeignKey(
        'companies.Company', on_delete=models.CASCADE, related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='mid'
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='fixed')
    is_onsite = models.BooleanField(default=True)
    is_remote = models.BooleanField(default=False)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='NPR')
    required_skills = models.JSONField(default=list, blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ImageField(upload_to='job_images/', null=True, blank=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        indexes = [
            models.Index(fields=['recruiter', 'is_active']),
            models.Index(fields=['company', 'is_active']),
            models.Index(fields=['job_type']),
            models.Index(fields=['experience_level']),
            models.Index(fields=['created_at']),
        ]

    @property
    def applications_count(self):
        return self.applications.count()

    def __str__(self):
        return f"{self.title} @ {self.company.name} [{self.get_job_type_display()}]"
