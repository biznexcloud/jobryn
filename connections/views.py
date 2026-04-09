from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Connection
from .serializers import ConnectionSerializer, ConnectionUpdateSerializer


class SendConnectionRequestView(generics.CreateAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class RespondConnectionRequestView(generics.UpdateAPIView):
    serializer_class = ConnectionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Connection.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Only receiver can respond
        if instance.receiver != request.user:
            return Response(
                {"detail": "You are not allowed to respond to this request."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        status_value = serializer.validated_data.get('status')

        if status_value == 'accepted':
            instance.accepted_at = timezone.now()

        instance.status = status_value
        instance.save()

        return Response({"detail": f"Connection {status_value}."})


class CancelConnectionRequestView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')

        try:
            connection = Connection.objects.get(id=connection_id, sender=request.user)

            if connection.status != 'pending':
                return Response(
                    {"detail": "Only pending requests can be cancelled."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            connection.delete()
            return Response(
                {"detail": "Connection request cancelled."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Connection.DoesNotExist:
            return Response(
                {"detail": "Connection not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class ConnectionListView(generics.ListAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Connection.objects.filter(
            sender=user
        ).select_related('receiver')


class IncomingConnectionListView(generics.ListAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Connection.objects.filter(
            receiver=user
        ).select_related('sender')