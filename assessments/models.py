from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta

# Assuming you have a central 'skills' app or model to link this to.
# If not, you can replace it with a CharField choice or a local Skill model.
# from apps.skills.models import Skill 

class Assessment(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='assessments')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    
    # Rules & Configs
    time_limit = models.DurationField(
        help_text="Time allowed to complete the assessment (e.g., 00:15:00 for 15 mins)",
        default=timedelta(minutes=15)
    )
    passing_score = models.PositiveIntegerField(
        default=70, 
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Percentage required to pass (e.g., 70 for 70%)"
    )
    retake_cooldown_days = models.PositiveIntegerField(
        default=30,
        help_text="Number of days a user must wait before retaking this assessment if they fail."
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"


class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The question prompt.")
    explanation = models.TextField(
        blank=True, 
        help_text="Explanation shown to the user *after* the entire quiz is graded."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.text[:50]}..."


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(
        default=False,
        help_text="Designate if this choice is the correct answer."
    )

    def __str__(self):
        return f"{self.text[:30]} ({'Correct' if self.is_correct else 'Wrong'})"


class AssessmentAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Final calculated percentage score."
    )
    is_passed = models.BooleanField(default=False)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.email} - {self.assessment.title} ({self.status})"

    @property
    def time_remaining(self):
        """Calculates remaining time for the frontend countdown timer."""
        if self.status != 'in_progress':
            return timedelta(0)
        
        elapsed = timezone.now() - self.started_at
        remaining = self.assessment.time_limit - elapsed
        return max(remaining, timedelta(0))


class UserAssessmentBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='badges_issued')
    attempt = models.OneToOneField(AssessmentAttempt, on_delete=models.CASCADE, related_name='earned_badge')
    
    issued_at = models.DateTimeField(auto_now_add=True)
    badge_revocation_date = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="If certifications/badges expire (e.g., after 1 or 2 years)."
    )

    class Meta:
        unique_together = ('user', 'assessment')  # A user can only hold one active badge per assessment topic.

    def __str__(self):
        return f"Badge: {self.user.email} verified in {self.assessment.title}"

