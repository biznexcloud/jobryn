from rest_framework import serializers
from .models import Recommended

class seekersRecommendedSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    company_name = serializers.ReadOnlyField(source='company.name')
    
    class Meta:
        model = Recommended
        fields = (
            'id', 'job', 'job_title', 'company', 'company_name', 
            'education', 'skills', 'experience', 'projects', 
            'created_at'
        )
        read_only_fields = ('id', 'created_at',)

class RecruiterRecommendedSerializer(serializers.ModelSerializer):
    education_level = serializers.ReadOnlyField(source='education.degree')
    skills_name = serializers.ReadOnlyField(source='skills.name')
    experience_name = serializers.ReadOnlyField(source='experience.title')
    projects_title = serializers.ReadOnlyField(source='projects.name')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Recommended
        fields = (
            'id', 'job', 'education', 'education_level', 
            'skills', 'skills_name', 'experience', 'experience_name', 
            'projects', 'projects_title', 'company', 'user', 
            'user_email', 'created_at'
        )
        read_only_fields = ('id', 'created_at',)
