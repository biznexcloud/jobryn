from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Connection
from .serializers import (
    ConnectionReadSerializer, 
    ConnectionCreateSerializer, 
    ConnectionUpdateStatusSerializer
)
# Assuming your permission classes are defined here or imported
from jobrynbackend.permissions import IsEmailVerified, IsConnectionParty

class ConnectionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Production ViewSet managing user-to-user business networking lifecycles.
    """
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get_queryset(self):
        user = self.request.user
        # Admins see global scopes; users only see instances they participate in
        if hasattr(user, 'role') and user.role == 'admin':
            return Connection.objects.select_related('sender', 'receiver').all()
            
        return Connection.objects.select_related('sender', 'receiver').filter(
            Q(sender=user) | Q(receiver=user)
        ).exclude(status='blocked') # Hide blocked relations dynamically by default

    def get_serializer_class(self):
        if self.action == 'create':
            return ConnectionCreateSerializer
        if self.action in ['update_status', 'partial_update']:
            return ConnectionUpdateStatusSerializer
        return ConnectionReadSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'], url_path='update-status', permission_classes=[IsAuthenticated, IsConnectionParty])
    def update_status(self, request, pk=None):
        """
        Dedicated endpoint to mutate status state maps.
        PATCH /api/connections/{id}/update-status/ -> data: {"status": "accepted"}
        """
        connection = self.get_object()
        serializer = self.get_serializer(connection, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        updated_connection = serializer.save()
        
        return Response(ConnectionReadSerializer(updated_connection).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='invitations/received')
    def received_invitations(self, request):
        """Fetch incoming pending connection invites."""
        queryset = self.get_queryset().filter(receiver=request.user, status='pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ConnectionReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = ConnectionReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='network')
    def network_list(self, request):
        """Fetch all actively accepted network nodes."""
        queryset = self.get_queryset().filter(status='accepted')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ConnectionReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ConnectionReadSerializer(queryset, many=True)
        return Response(serializer.data)