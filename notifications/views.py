from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('sender')


class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).select_related('sender')


class CreateNotificationView(generics.CreateAPIView):
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarkNotificationAsReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()

        if notification.recipient != request.user:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

        return Response({"detail": "Notification marked as read."})


class MarkAllAsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )

        return Response({
            "detail": f"{updated} notifications marked as read."
        })


class DeleteNotificationView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def delete(self, request, *args, **kwargs):
        notification = self.get_object()

        if notification.recipient != request.user:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        notification.delete()
        return Response(
            {"detail": "Notification deleted."},
            status=status.HTTP_204_NO_CONTENT
        )