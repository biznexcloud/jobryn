from django.db import models
from django.conf import settings

class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    skills_used = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)  # Whether to show this experience on the public profile

    # 👔 PROFESSIONAL DETAILS
    EMPLOYMENT_TYPES = (
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    )
    LOCATION_TYPES = (
        ('on-site', 'On-site'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    )
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='full-time')
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='on-site')
    company_logo = models.ImageField(upload_to='experience_logos/', null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company_name} ({self.user.email})"
