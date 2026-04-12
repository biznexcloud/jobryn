from rest_framework import viewsets, permissions
from .models import Meeting

from .serializers import JobSeeker_MeetingSerializer, Recruiter_MeetingSerializer
from jobrynbackend.permissions import IsJobSeeker, IsRecruiter

class JobSeeker_MeetingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for Job Seekers to view their scheduled meetings.
    """
    serializer_class = JobSeeker_MeetingSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Meeting.objects.none()
        return Meeting.objects.filter(application__seeker=self.request.user)

class Recruiter_MeetingViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to schedule and manage meetings/interviews.
    """
    serializer_class = Recruiter_MeetingSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Meeting.objects.none()
        return Meeting.objects.filter(application__job__recruiter=self.request.user)
