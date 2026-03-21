from django.db import models
from django.conf import settings


class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('design', 'Design'),
        ('management', 'Management'),
        ('communication', 'Communication'),
        ('data', 'Data & Analytics'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('language', 'Language'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='technical')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} [{self.get_category_display()}]"


class UserSkill(models.Model):
    PROFICIENCY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
        ('master', 'Master'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate')
    years_of_experience = models.PositiveSmallIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')
        indexes = [
            models.Index(fields=['user', 'proficiency_level']),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.skill.name} [{self.get_proficiency_level_display()}]"


class Endorsement(models.Model):
    endorser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_endorsements'
    )
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE, related_name='endorsements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('endorser', 'user_skill')

    def __str__(self):
        return f"{self.endorser.email} endorsed {self.user_skill}"
