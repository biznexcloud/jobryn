from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from jobrynbackend.permissions import IsOwnerOrReadOnly, IsEmailVerified, IsJobSeeker


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_deleted=False).select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_edited=True)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    # 🔥 LIKE / UNLIKE TOGGLE
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()
            post.likes_count = F('likes_count') - 1
            post.save()
            return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)

        post.likes_count = F('likes_count') + 1
        post.save()
        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

# class PostVisibilityViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

#     @action(detail=True, methods=['post'])
#     def set_visibility(self, request, pk=None):
#         post = Post.objects.filter(pk=pk, author=request.user).first()
#         if not post:
#             return Response({'error': 'Post not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)

#         visibility = request.data.get('visibility')
#         if visibility not in ['public', 'connections', 'private']:
#             return Response({'error': 'Invalid visibility option'}, status=status.HTTP_400_BAD_REQUEST)

#         post.visibility = visibility
#         post.save()
#         return Response({'message': f'Visibility set to {visibility}'}, status=status.HTTP_200_OK)
    
# class PostShareViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated, IsEmailVerified, IsJobSeeker]

#     @action(detail=True, methods=['post'])
#     def share(self, request, pk=None):
#         original_post = Post.objects.filter(pk=pk, is_deleted=False).first()
#         if not original_post:
#             return Response({'error': 'Original post not found'}, status=status.HTTP_404_NOT_FOUND)

#         content = request.data.get('content', '')
#         visibility = request.data.get('visibility', 'connections')

#         if visibility not in ['public', 'connections', 'private']:
#             return Response({'error': 'Invalid visibility option'}, status=status.HTTP_400_BAD_REQUEST)

#         shared_post = Post.objects.create(
#             author=request.user,
#             content=content,
#             visibility=visibility,
#             shared_post=original_post
#         )

#         serializer = PostSerializer(shared_post, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_201_CREATED)    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(post__is_deleted=False).select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(is_edited=True)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        qs = super().get_queryset()
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().select_related('user', 'post')
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        qs = super().get_queryset()
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs
    
    def perform_destroy(self, instance):
        instance.delete()
    
