from rest_framework import serializers
from .models import Job

class JobSeeker_JobSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    
    class Meta:
        model = Job
        fields = (
            'id', 'company', 'company_name', 'title', 'description', 
            'location', 'job_type', 'experience_level', 'payment_type', 
            'is_onsite', 'is_remote', 'salary_min', 'salary_max', 
            'currency', 'required_skills', 'requirements', 'benefits', 
            'application_deadline', 'created_at'
        )
        read_only_fields = ('created_at',)

class Recruiter_JobSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('recruiter', 'created_at', 'updated_at', 'views_count')

class JobDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'views_count')
