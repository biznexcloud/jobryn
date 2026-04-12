from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Job
from jobrynbackend.permissions import IsRecruiter, IsJobSeeker
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import JobSeeker_JobSerializer, Recruiter_JobSerializer

class JobSeeker_JobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for Job Seekers to discover active jobs.
    """
    serializer_class = JobSeeker_JobSerializer
    permission_classes = [IsJobSeeker]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['job_type', 'experience_level', 'is_onsite', 'is_remote', 'payment_type']
    search_fields = ['title', 'description', 'location', 'company__name']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    ordering = ['-created_at']

    def get_queryset(self):
        return Job.objects.select_related('company').filter(is_active=True)

class Recruiter_JobViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to manage their own job postings.
    """
    serializer_class = Recruiter_JobSerializer
    permission_classes = [IsRecruiter]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Job.objects.none()
        return Job.objects.select_related('company').filter(recruiter=self.request.user)

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Recruiter can toggle job active/inactive."""
        job = self.get_object()
        job.is_active = not job.is_active
        job.save()
        return Response({'is_active': job.is_active})
