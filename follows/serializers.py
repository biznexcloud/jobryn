from rest_framework import serializers
from account.models import User
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.id')
    follower_email = serializers.ReadOnlyField(source='follower.email')
    following_email = serializers.ReadOnlyField(source='following.email')

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower',
            'follower_email',
            'following',
            'following_email',
            'follow_type',
            'created_at',
        ]
        read_only_fields = ['id', 'follower', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        follower = request.user
        following = attrs.get('following')

        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself.")

        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError("Already following this user.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['follower'] = request.user
        return super().create(validated_data)