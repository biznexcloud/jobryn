from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # 🧍 MEDIA
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    
    # 📄 BASIC INFO
    headline = models.CharField(max_length=220, blank=True)
    about = models.TextField(blank=True)
    pronouns = models.CharField(max_length=50, blank=True)
    user_strength = models.CharField(max_length=255, blank=True)  # e.g. "Creative Problem Solver"
    user_weakness = models.CharField(max_length=255, blank=True)  # e.g. "Perfectionist"
    
    # 📍 LOCATION
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    
    # 💼 PROFESSIONAL INFO
    job_title = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.FloatField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    
    # 📄 DOCUMENTS & LINKS
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    portfolio_url = models.URLField(null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    
    # 🧠 EXTRAS
    featured_items = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    
    
    # 🕵️ VISIBILITY & AVAILABILITY
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('connections', 'Connections Only'),
    )
    visibility_settings = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    available_for_freelance = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)  # open to work
    professional_motto = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    @property
    def profile_strength(self):
        strength = 0
        if self.headline: strength += 10
        if self.about: strength += 15
        if self.profile_picture: strength += 10
        if self.city or self.country: strength += 10
        if self.resume: strength += 15
        if self.job_title: strength += 10
        if self.skills: strength += 15
        if self.education: strength += 15
        return min(strength, 100)

    def __str__(self):
        return f"{self.user.email} Profile"
