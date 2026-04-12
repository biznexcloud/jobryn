from django.shortcuts import render
from .serializers import seekersRecommendedSerializer, RecruiterRecommendedSerializer
from rest_framework import generics, permissions
from jobrynbackend.permissions import IsRecruiter, IsJobSeeker
from .models import Recommended
from rest_framework import viewsets

# Create your views here.
class SeekersRecommendedList(viewsets.ReadOnlyModelViewSet):
    queryset = Recommended.objects.all()
    serializer_class = seekersRecommendedSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        user = self.request.user
        return Recommended.objects.filter(user=user).select_related('job', 'company', 'education', 'skills', 'experience', 'projects')

class RecruiterRecommendedList(viewsets.ReadOnlyModelViewSet):
    queryset = Recommended.objects.all()
    serializer_class = RecruiterRecommendedSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        user = self.request.user
        return Recommended.objects.filter(company__recruiter=user).select_related('job', 'company', 'education', 'skills', 'experience', 'projects', 'user')    
    
    
