from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Connection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('blocked', 'Blocked'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_connections'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_connections'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # LinkedIn-style enhancements
    message = models.TextField(blank=True, max_length=500, help_text="Optional invitation message.")
    category = models.CharField(max_length=50, blank=True, help_text="E.g., Colleague, Classmate, Client")
    
    # Lifecycle Timestamps
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

        indexes = [
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
            models.Index(fields=['status']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=~models.Q(sender=models.F('receiver')),
                name='prevent_self_connection'
            )
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} [{self.status}]"

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("You cannot establish a connection with yourself.")
        
        # Prevent reverse duplicates (If B already invited A, A should accept instead of creating a new inverse row)
        if not self.pk and Connection.objects.filter(sender=self.receiver, receiver=self.sender).exists():
            raise ValidationError("An inverse connection request already exists between these users.")

    def save(self, *custom_args, **kwargs):
        self.full_clean()
        # Set accepted timestamp dynamically if status transitioned
        if self.status == 'accepted' and not self.accepted_at:
            self.accepted_at = timezone.now()
        elif self.status != 'accepted':
            self.accepted_at = None
        super().save(*custom_args, **kwargs)