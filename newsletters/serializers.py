from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Newsletter, Subscriber

User = get_user_model()


# -------------------------
# Subscriber Serializer
# -------------------------
class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = [
            'id',
            'email',
            'user',
            'is_active',
            'subscribed_at',
            'unsubscribed_at'
        ]
        read_only_fields = ['id', 'user', 'subscribed_at', 'unsubscribed_at']

    def create(self, validated_data):
        request = self.context.get('request')
        email = validated_data.get('email')

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={
                'user': request.user if request and request.user.is_authenticated else None
            }
        )

        if not created:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()

        return subscriber


# -------------------------
# Newsletter Serializer
# -------------------------
class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
        read_only_fields = ['id', 'status', 'sent_at', 'created_at']


class NewsletterSendSerializer(serializers.Serializer):
    newsletter_id = serializers.IntegerField()

    def validate_newsletter_id(self, value):
        try:
            newsletter = Newsletter.objects.get(id=value)
        except Newsletter.DoesNotExist:
            raise serializers.ValidationError("Newsletter not found")

        if newsletter.status == 'sent':
            raise serializers.ValidationError("Already sent")

        return value