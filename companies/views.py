from rest_framework import viewsets, permissions
from .models import Company
from .serializers import CompanySerializer
from jobrynbackend.permissions import IsRecruiter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'recruiter':
            return Company.objects.filter(owner=user)
        return Company.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['industry', 'location', 'company_size']
    search_fields = ['name', 'description', 'location', 'industry']
    ordering_fields = ['created_at', 'name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
