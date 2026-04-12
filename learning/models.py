from django.db import models
from django.conf import settings


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructed_courses'
    )
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    language = models.CharField(max_length=50, default='English')
    syllabus = models.TextField(blank=True)
    what_you_learn = models.JSONField(default=list, blank=True)
    requirements = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_hours = models.PositiveIntegerField(default=0)
    total_lectures = models.PositiveIntegerField(default=0)
    certificate_offered = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        indexes = [
            models.Index(fields=['instructor', 'is_published']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.title} [{self.get_level_display()}]"


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    progress = models.PositiveSmallIntegerField(default=0)  # 0–100%
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    certificate_issued = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return f"{self.user.email} in {self.course.title} ({self.progress}%)"
