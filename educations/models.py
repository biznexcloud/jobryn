from django.db import models
from django.conf import settings

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=255, blank=True)
    certificate = models.FileField(upload_to='education_certificates/', null=True, blank=True)
    is_public = models.BooleanField(default=True)  # Whether to show this education on the public profile
    
    # 🎓 ACADEMIC DETAILS
    activities_societies = models.TextField(blank=True)
    gpa_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.school} - {self.degree} ({self.user.email})"
