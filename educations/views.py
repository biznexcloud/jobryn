from rest_framework import viewsets, permissions
from .models import Education
from .serializers import EducationSerializer

class IsEducationOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsEducationOwnerOrReadOnly]
    filterset_fields = ['school', 'degree']
    search_fields = ['school', 'field_of_study', 'description']

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        qs = Education.objects.all().select_related('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
