# serializers.py

from rest_framework import serializers
from .models import (
    Assessment,
    Question,
    Choice,
    AssessmentAttempt,
    UserAssessmentBadge
)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class AdminChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'explanation',
            'choices',
        ]


class AdminQuestionSerializer(serializers.ModelSerializer):
    choices = AdminChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'explanation',
            'choices',
        ]


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = [
            'id',
            'title',
            'description',
            'difficulty',
            'time_limit',
            'passing_score',
            'retake_cooldown_days',
            'is_active',
            'questions',
            'created_at',
            'updated_at',
        ]


class AssessmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            'id',
            'title',
            'difficulty',
            'time_limit',
            'passing_score',
            'is_active',
        ]


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    assessment = AssessmentListSerializer(read_only=True)
    time_remaining = serializers.ReadOnlyField()

    class Meta:
        model = AssessmentAttempt
        fields = [
            'id',
            'assessment',
            'status',
            'score',
            'is_passed',
            'started_at',
            'completed_at',
            'time_remaining',
        ]


class UserAssessmentBadgeSerializer(serializers.ModelSerializer):
    assessment = AssessmentListSerializer(read_only=True)

    class Meta:
        model = UserAssessmentBadge
        fields = [
            'id',
            'assessment',
            'issued_at',
            'badge_revocation_date',
        ]