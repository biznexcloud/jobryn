from rest_framework import viewsets, permissions
from .models import Experience
from .serializers import ExperienceSerializer

class IsExperienceOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsExperienceOwnerOrReadOnly]
    filterset_fields = ['company_name', 'is_current']
    search_fields = ['title', 'company_name', 'description']

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        qs = Experience.objects.all().select_related('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
