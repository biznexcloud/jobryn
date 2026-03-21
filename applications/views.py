from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Application
from jobrynbackend.permissions import IsRecruiter, IsJobSeeker


from .serializers import JobSeeker_ApplicationSerializer, Recruiter_ApplicationSerializer

class JobSeeker_ApplicationViewSet(viewsets.ModelViewSet):
    """
    API for Job Seekers to manage their own applications.
    """
    serializer_class = JobSeeker_ApplicationSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Application.objects.none()
        return Application.objects.select_related('job', 'job__company').filter(seeker=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seeker=self.request.user)

    @action(detail=True, methods=['patch'])
    def withdraw(self, request, pk=None):
        """Job seeker withdraws their application."""
        application = self.get_object()
        if application.status in ['hired', 'rejected']:
            return Response({'error': 'Cannot withdraw finalized application.'}, status=400)
        application.status = 'withdrawn'
        application.save()
        return Response({'status': 'withdrawn'})

class Recruiter_ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for Recruiters to view and manage applications for their jobs.
    """
    serializer_class = Recruiter_ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Application.objects.none()
        return Application.objects.select_related('job', 'seeker', 'job__company').filter(
            job__recruiter=self.request.user
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Recruiter updates application status."""
        application = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = [s[0] for s in Application.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Choose from: {valid_statuses}'}, status=400)

        application.status = new_status
        if new_status == 'hired':
            application.hired_at = timezone.now()
            application.accepted_salary = request.data.get('accepted_salary', application.expected_salary)
            application.payment_type = application.job.payment_type
        elif new_status == 'rejected':
            application.rejection_reason = request.data.get('rejection_reason', '')
        application.save()
        return Response(Recruiter_ApplicationSerializer(application).data)
