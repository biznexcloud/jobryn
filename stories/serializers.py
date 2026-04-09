from .models import Stori, StoriLike, StoriView, StoriComment
from rest_framework import serializers

class StoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stori
        fields = [ 'id', 'author', 'caption', 'images', 'visibility', 'is_active', 'views_count', 'likes_count']
        read_only_fields = ['id', 'author', 'views_count', 'likes_count', 'created_at']

        def perform_create(self, serializer):
        
            serializer.save(author=self.request.user)

        
    # def create(self, validated_data):
    #     images = validated_data.pop('images', [])
    #     story = Stori.objects.create(**validated_data)

    #     # if using separate StoriMedia model
    #     for image in images:
    #         Stori.objects.create(
    #             story=story,
    #             file=image,
    #             media_type='image'
    #         )

    #     return story

class StoriLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriLike
        fields = ['id', 'story', 'user', 'created_at']
        read_only_fields = ['id', 'story', 'user', 'created_at']

class StoriViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriView
        fields = ['id', 'story', 'user', 'viewed_at']
        read_only_fields = ['id', 'story', 'user', 'viewed_at']

class StoriCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriComment
        fields = ['id', 'story', 'author', 'content', 'parent', 'created_at']
        read_only_fields = ['id', 'story', 'author', 'created_at']