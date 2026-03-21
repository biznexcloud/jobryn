from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
from .models import User

@receiver(post_save, sender=User)
def send_welcome_and_otp_email(sender, instance, created, **kwargs):
    if created:
        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))
        expiry = timezone.now() + timezone.timedelta(minutes=10)
        
        # Update using QuerySet to avoid triggering save() again and infinite loops
        User.objects.filter(pk=instance.pk).update(otp=otp, otp_expiry=expiry)
        
        # For the current instance in memory (optional but good practice)
        instance.otp = otp
        instance.otp_expiry = expiry

        subject = "Welcome to Jobryn - Verify your email"
        message = f"Hi {instance.name or 'User'},\n\nWelcome to Jobryn! We're excited to have you on board.\n\nYour OTP for email verification is: {otp}\nThis OTP is valid for 10 minutes.\n\nBest regards,\nThe Jobryn Team"
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            # Optionally log the error if email fails
            print(f"Error sending email: {e}")
