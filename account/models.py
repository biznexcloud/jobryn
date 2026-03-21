from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )

    # 🔐 AUTH CORE
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    
    # ✉️ EMAIL VERIFICATION
    is_email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker', db_index=True)

    # 📱 CONTACT
    phone = PhoneNumberField(region='NP', null=True, blank=True)
    alternate_phone = PhoneNumberField(region='NP', null=True, blank=True)

    # 🧠 SECURITY & VERIFICATION
    is_identity_verified = models.BooleanField(default=False)
    is_verified_recruiter = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)

    # 🌍 LOCALIZATION
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=100, default='Asia/Kathmandu')

    # ⚙️ SYSTEM
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=['email', 'role', 'is_active']),
        ]

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"