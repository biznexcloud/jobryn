from rest_framework import serializers
from .models import Meeting

class JobSeeker_MeetingSerializer(serializers.ModelSerializer):
    meeting_type_display = serializers.CharField(source='get_meeting_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'application', 'meeting_type', 'meeting_type_display', 
            'scheduled_at', 'meeting_link', 'location_address', 
            'duration_minutes', 'agenda', 'status', 'status_display', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('status', 'created_at', 'updated_at')

class Recruiter_MeetingSerializer(serializers.ModelSerializer):
    meeting_type_display = serializers.CharField(source='get_meeting_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    seeker_name = serializers.ReadOnlyField(source='application.seeker.name')

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
