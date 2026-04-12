from rest_framework import viewsets, permissions
from .models import Profile
from .serializers import JobSeeker_ProfileSerializer, Recruiter_ProfileSerializer
from jobrynbackend.permissions import IsJobSeeker, IsRecruiter

class JobSeeker_ProfileViewSet(viewsets.ModelViewSet):
    """
    API for Job Seekers to manage their own profile.
    """
    serializer_class = JobSeeker_ProfileSerializer
    permission_classes = [IsJobSeeker, permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Recruiter_ProfileViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to manage their own profile.
    """
    serializer_class = Recruiter_ProfileSerializer
    permission_classes = [IsRecruiter, permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
