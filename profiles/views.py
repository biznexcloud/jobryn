from rest_framework import viewsets, permissions
from .models import Profile
from .serializers import JobSeeker_ProfileSerializer, Recruiter_ProfileSerializer
from jobrynbackend.permissions import IsJobSeeker, IsRecruiter

# class JobSeeker_ProfileViewSet(viewsets.ModelViewSet):
#     """
#     API for Job Seekers to manage their own profile.
#     """
#     serializer_class = JobSeeker_ProfileSerializer
#     permission_classes = [IsJobSeeker, permissions.IsAuthenticated]

#     def get_queryset(self):
#         if getattr(self, "swagger_fake_view", False):
#             return Profile.objects.none()
#         return Profile.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class Recruiter_ProfileViewSet(viewsets.ModelViewSet):
#     """
#     API for Recruiters to manage their own profile.
#     """
#     serializer_class = Recruiter_ProfileSerializer
#     permission_classes = [IsRecruiter, permissions.IsAuthenticated]

#     def get_queryset(self):
#         if getattr(self, "swagger_fake_view", False):
#             return Profile.objects.none()
#         return Profile.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

from django.db.models import Q

class JobSeeker_ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobSeeker_ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # public profiles
        public_profiles = Q(visibility_settings='public')

        # own profile
        own_profile = Q(user=user)

        # connected users
        connected_user_ids = Connection.objects.filter(
            Q(sender=user) | Q(receiver=user),
           status= 'accepted'
        ).values_list('sender', 'receiver')

        flat_ids = set()

        for sender, receiver in connected_user_ids:
            flat_ids.add(sender)
            flat_ids.add(receiver)

        connections_profiles = Q(
            visibility_settings='connections',
            user_id__in=flat_ids
        )

        return Profile.objects.filter(
            public_profiles |
            own_profile |
            connections_profiles
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Recruiter_ProfileViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to manage their own profile.
    """
    serializer_class = Recruiter_ProfileSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
