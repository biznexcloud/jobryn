from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from jobrynbackend.permissions import IsJobSeeker


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Courses API — Admin creates/manages, both roles can read.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.none()  # Required by DRF router

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Course.objects.select_related('instructor').filter(is_published=True)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    Enrollments API.
    - Job Seekers: Enroll + view/manage their own enrollments.
    - Recruiters: View enrollments in courses they instruct.
    """
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.none()  # Required by DRF router

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsJobSeeker()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Enrollment.objects.none()
        if user.role == 'recruiter':
            # Recruiters see enrollments in their courses
            return Enrollment.objects.select_related('user', 'course').filter(course__instructor=user)
        # Job seekers see their own enrollments
        return Enrollment.objects.select_related('course').filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        """Job seeker updates their own course progress."""
        enrollment = self.get_object()
        if enrollment.user != request.user:
            return Response({'error': 'Not your enrollment.'}, status=403)
        progress = request.data.get('progress', enrollment.progress)
        enrollment.progress = min(int(progress), 100)
        if enrollment.progress == 100:
            from django.utils import timezone
            enrollment.completed = True
            enrollment.completion_date = timezone.now()
        enrollment.save()
        return Response({'progress': enrollment.progress, 'completed': enrollment.completed})
