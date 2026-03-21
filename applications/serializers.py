from rest_framework import serializers
from .models import Application

class JobSeeker_ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    
    class Meta:
        model = Application
        fields = (
            'id', 'job', 'job_title', 'status', 'resume', 'cover_letter', 
            'expected_salary', 'rejection_reason', 'feedback_for_seeker', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('status', 'rejection_reason', 'feedback_for_seeker', 'created_at', 'updated_at')

class Recruiter_ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    seeker_name = serializers.ReadOnlyField(source='seeker.name')
    seeker_email = serializers.ReadOnlyField(source='seeker.email')

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('seeker', 'created_at', 'updated_at', 'commission_paid')
