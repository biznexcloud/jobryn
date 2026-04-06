from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following_id = kwargs.get('pk')

        try:
            follow = Follow.objects.get(
                follower=request.user,
                following_id=following_id
            )
            follow.delete()
            return Response(
                {"detail": "Unfollowed successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Follow.DoesNotExist:
            return Response(
                {"detail": "Not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return Follow.objects.filter(following_id=user_id).select_related('follower')


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return Follow.objects.filter(follower_id=user_id).select_related('following')
