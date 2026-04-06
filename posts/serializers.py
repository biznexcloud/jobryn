from rest_framework import serializers
from .models import Like, Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_email',
            'content', 'image', 'video',
            'visibility',
            'likes_count', 'comments_count',
            'is_edited', 'shared_post',
            'created_at', 'updated_at',
            'is_deleted', 'is_liked', 'is_saved'
        ]
        read_only_fields = ['author', 'likes_count', 'comments_count', 'is_edited']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_email', 'content', 'created_at']
        read_only_fields = ['author']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user']