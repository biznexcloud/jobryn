from django.db import models
from companies.models import Company
from jobs.models import Job
from educations.models import Education
from skills.models import Skill
from experiences.models import Experience
from projects.models import Project
from account.models import User


# Create your models here.
class Recommended(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommended_jobs')
    education =models.ForeignKey(Education, on_delete=models.CASCADE, related_name='recommended_education')
    skills =models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='recommended_skills')
    experience =models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='recommended_experience') 
    projects =models.ForeignKey(Project, on_delete=models.CASCADE, related_name='recommended_projects')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recommended_company')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommended_by_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        

    def __str__(self):
        return f"Recommended for {self.user.username}"
    
    