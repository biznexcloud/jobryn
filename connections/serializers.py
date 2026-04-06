from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Connection

User = get_user_model()


class ConnectionSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')
    sender_email = serializers.ReadOnlyField(source='sender.email')
    receiver_email = serializers.ReadOnlyField(source='receiver.email')

    class Meta:
        model = Connection
        fields = [
            'id',
            'sender',
            'sender_email',
            'receiver',
            'receiver_email',
            'status',
            'notes',
            'category',
            'accepted_at',
            'created_at',
        ]
        read_only_fields = ['id', 'sender', 'status', 'accepted_at', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        sender = request.user
        receiver = attrs.get('receiver')

        if sender == receiver:
            raise serializers.ValidationError("You cannot send connection request to yourself.")

        if Connection.objects.filter(sender=sender, receiver=receiver).exists():
            raise serializers.ValidationError("Connection request already exists.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class ConnectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['status']

    def validate_status(self, value):
        if value not in ['accepted', 'declined', 'blocked']:
            raise serializers.ValidationError("Invalid status update.")
        return value