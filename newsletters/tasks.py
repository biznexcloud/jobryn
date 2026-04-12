from celery import shared_task
from django.core.mail import send_mass_mail
from django.utils import timezone
from .models import Newsletter, Subscriber


@shared_task
def send_newsletter_task(newsletter_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        subscribers = Subscriber.objects.filter(is_active=True)

        messages = [
            (
                newsletter.subject or newsletter.title,
                newsletter.content,
                None,
                [sub.email],
            )
            for sub in subscribers
        ]

        send_mass_mail(messages, fail_silently=False)

        newsletter.status = 'sent'
        newsletter.sent_at = timezone.now()
        newsletter.save()

        return "Newsletter sent"

    except Exception as e:
        return str(e)