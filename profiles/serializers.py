from rest_framework import serializers
from .models import Profile
from account.serializers import UserSerializer

class JobSeeker_ProfileSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    profile_strength = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'profile_strength']

class Recruiter_ProfileSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_detail', 'headline', 'about', 'profile_picture','cover_image', 'visibility_settings']
        read_only_fields = ['user']
