from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        if not data.get('is_current') and not data.get('end_date'):
            raise serializers.ValidationError("End date is required if this is not a current position.")
        if data.get('end_date') and data.get('start_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data
