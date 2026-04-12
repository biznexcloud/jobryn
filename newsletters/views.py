from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mass_mail
from .models import Newsletter, Subscriber
from .serializers import (
    NewsletterSerializer,
    SubscriberSerializer,
    NewsletterSendSerializer
)


# -------------------------
# Subscribe / Unsubscribe
# -------------------------
class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscriberSerializer


class UnsubscribeView(generics.GenericAPIView):
    serializer_class = SubscriberSerializer

    def post(self, request):
        email = request.data.get('email')

        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()

            return Response({"detail": "Unsubscribed successfully"})
        except Subscriber.DoesNotExist:
            return Response({"detail": "Email not found"}, status=404)


# -------------------------
# Newsletter CRUD
# -------------------------
class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAdminUser]


class NewsletterListView(generics.ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAdminUser]


# -------------------------
# Send Newsletter
# -------------------------
class SendNewsletterView(generics.GenericAPIView):
    serializer_class = NewsletterSendSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        newsletter = Newsletter.objects.get(
            id=serializer.validated_data['newsletter_id']
        )

        subscribers = Subscriber.objects.filter(is_active=True)

        if not subscribers.exists():
            return Response({"detail": "No active subscribers"}, status=400)

        messages = []
        for sub in subscribers:
            messages.append((
                newsletter.subject or newsletter.title,
                newsletter.content,
                None,
                [sub.email],
            ))

        send_mass_mail(messages, fail_silently=False)

        newsletter.status = 'sent'
        newsletter.sent_at = timezone.now()
        newsletter.save()

        return Response({"detail": "Newsletter sent successfully"})