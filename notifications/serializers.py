from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'sender',
            'sender_email',
            'notification_type',
            'title',
            'message',
            'is_read',
            'read_at',
            'action_url',
            'related_object_id',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'recipient',
            'sender',
            'is_read',
            'read_at',
            'created_at',
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'recipient',
            'notification_type',
            'title',
            'message',
            'action_url',
            'related_object_id',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user if request else None
        return super().create(validated_data)