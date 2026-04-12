from django.db import models
from django.conf import settings

class Certification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user.email}"
