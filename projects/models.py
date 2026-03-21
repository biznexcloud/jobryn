from django.db import models
from django.conf import settings

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True)
    role = models.CharField(max_length=100, blank=True)
    technologies = models.JSONField(default=list, blank=True)
    
    # 🏗️ REPOSITORY & TEAM
    repository_url = models.URLField(blank=True)
    collaborators = models.JSONField(default=list, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"
