from rest_framework import serializers
from .models import Skill, UserSkill, Endorsement

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class EndorsementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endorsement
        fields = '__all__'
        read_only_fields = ['endorser']

    def validate(self, data):
        if data['user_skill'].user == self.context['request'].user:
            raise serializers.ValidationError("You cannot endorse your own skill.")
        return data

class UserSkillSerializer(serializers.ModelSerializer):
    skill_detail = SkillSerializer(source='skill', read_only=True)
    endorsement_count = serializers.SerializerMethodField()

    class Meta:
        model = UserSkill
        fields = '__all__'
        read_only_fields = ['user']

    def get_endorsement_count(self, obj):
        return obj.endorsements.count()
