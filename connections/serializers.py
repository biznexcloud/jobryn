from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Connection

User = get_user_model()

class ConnectionUserSerializer(serializers.ModelSerializer):
    """Minimal user payload representing connection nodes."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'full_name', 'role']


class ConnectionReadSerializer(serializers.ModelSerializer):
    sender = ConnectionUserSerializer(read_only=True)
    receiver = ConnectionUserSerializer(read_only=True)

    class Meta:
        model = Connection
        fields = [
            'id', 'sender', 'receiver', 'status', 
            'message', 'category', 'accepted_at', 
            'created_at', 'updated_at'
        ]


class ConnectionCreateSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'message', 'category']

    def validate(self, attrs):
        sender = attrs['sender']
        receiver = attrs['receiver']

        if sender == receiver:
            raise serializers.ValidationError({"receiver": "You cannot send a connection request to yourself."})

        # Check for active existing requests in either direction
        exists_direct = Connection.objects.filter(sender=sender, receiver=receiver).exists()
        exists_inverse = Connection.objects.filter(sender=receiver, receiver=sender).exists()

        if exists_direct or exists_inverse:
            raise serializers.ValidationError("A connection setup or request already exists between you two.")

        return attrs


class ConnectionUpdateStatusSerializer(serializers.ModelSerializer):
    """Handles status changes securely. Only specific status pathways are permitted."""
    class Meta:
        model = Connection
        fields = ['status']

    def validate_status(self, value):
        allowed_statuses = ['accepted', 'declined', 'blocked']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Invalid status selection. Choose from: {', '.join(allowed_statuses)}.")
        return value

    def update(self, instance, validated_data):
        current_user = self.context['request'].user
        new_status = validated_data.get('status')

        # Logic Matrix for updates
        if new_status in ['accepted', 'declined']:
            # Only the explicit receiver can Accept or Decline a request
            if instance.receiver != current_user:
                raise serializers.ValidationError("Only the recipient can accept or decline this request.")
            if instance.status != 'pending':
                raise serializers.ValidationError(f"Cannot update status. The request is currently '{instance.status}'.")

        if new_status == 'blocked':
            # Anyone party to the connection can initiate a block state
            if current_user != instance.sender and current_user != instance.receiver:
                raise serializers.ValidationError("You are not part of this connection.")

        instance.status = new_status
        instance.save()
        return instance