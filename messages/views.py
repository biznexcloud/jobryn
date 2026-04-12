from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Message
from .serializers import MessageSerializer, MessageListSerializer


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ConversationView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs.get('user_id')

        return Message.objects.filter(
            Q(sender=user, receiver_id=other_user_id, is_deleted_by_sender=False) |
            Q(receiver=user, sender_id=other_user_id, is_deleted_by_receiver=False)
        ).select_related('sender').order_by('created_at')


class ThreadMessagesView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_id')
        user = self.request.user

        return Message.objects.filter(
            thread_id=thread_id
        ).filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        ).select_related('sender')
    
class MarkAsReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def update(self, request, *args, **kwargs):
        message = self.get_object()

        if message.receiver != request.user:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        message.is_read = True
        message.read_at = timezone.now()
        message.save()

        return Response({"detail": "Message marked as read."})


class DeleteMessageView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        user = request.user

        if message.sender == user:
            message.is_deleted_by_sender = True
        elif message.receiver == user:
            message.is_deleted_by_receiver = True
        else:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Hard delete if both deleted
        if message.is_deleted_by_sender and message.is_deleted_by_receiver:
            message.delete()
        else:
            message.save()

        return Response({"detail": "Message deleted."}, status=status.HTTP_204_NO_CONTENT)