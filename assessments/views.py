# views.py

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Assessment,
    AssessmentAttempt,
    UserAssessmentBadge
)

from .serializers import (
    AssessmentSerializer,
    AssessmentListSerializer,
    AssessmentAttemptSerializer,
    UserAssessmentBadgeSerializer
)


class AssessmentListAPIView(generics.ListAPIView):
    queryset = Assessment.objects.filter(is_active=True)
    serializer_class = AssessmentListSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssessmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Assessment.objects.filter(is_active=True)
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartAssessmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        assessment = get_object_or_404(
            Assessment,
            pk=pk,
            is_active=True
        )

        attempt = AssessmentAttempt.objects.create(
            user=request.user,
            assessment=assessment
        )

        serializer = AssessmentAttemptSerializer(attempt)

        return Response({
            'message': 'Assessment started successfully',
            'data': serializer.data
        })

class MyAttemptsAPIView(generics.ListAPIView):
    serializer_class = AssessmentAttemptSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(
            user=self.request.user
        )


class MyBadgesAPIView(generics.ListAPIView):
    serializer_class = UserAssessmentBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAssessmentBadge.objects.filter(
            user=self.request.user
        )