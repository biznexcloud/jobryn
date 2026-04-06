from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message
import uuid

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')
    sender_email = serializers.ReadOnlyField(source='sender.email')
    receiver_email = serializers.ReadOnlyField(source='receiver.email')

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_email',
            'receiver',
            'receiver_email',
            'content',
            'attachment',
            'thread_id',
            'is_read',
            'read_at',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'sender',
            'is_read',
            'read_at',
            'thread_id',
            'created_at',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        sender = request.user
        receiver = attrs.get('receiver')

        if sender == receiver:
            raise serializers.ValidationError("You cannot send message to yourself.")

        if not attrs.get('content') and not attrs.get('attachment'):
            raise serializers.ValidationError("Message must have content or attachment.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        sender = request.user
        receiver = validated_data.get('receiver')

        # Generate or reuse thread_id
        thread_id = validated_data.get('thread_id')

        if not thread_id:
            existing_thread = Message.objects.filter(
                sender=receiver,
                receiver=sender
            ).order_by('-created_at').first()

            if existing_thread:
                thread_id = existing_thread.thread_id
            else:
                thread_id = str(uuid.uuid4())

        validated_data['sender'] = sender
        validated_data['thread_id'] = thread_id

        return super().create(validated_data)


class MessageListSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')

    class Meta:
        model = Message
        fields = [
            'id',
            'sender_email',
            'content',
            'attachment',
            'is_read',
            'created_at',
        ]