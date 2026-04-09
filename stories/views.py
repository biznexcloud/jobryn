from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Stori, StoriLike, StoriView, StoriComment, StoriMedia
from .serializers import StoriSerializer, StoriLikeSerializer, StoriViewSerializer, StoriCommentSerializer, StoriMediaSerializer
# Create your views here.

class StoriViewSet(viewsets.ModelViewSet):
    queryset = Stori.objects.all()
    serializer_class = StoriSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    # def get_queryset(self):
    #     user = self.request.user
    #     return Stori.objects.filter(author=user)
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class StoriLikeViewSet(viewsets.ModelViewSet):
    queryset = StoriLike.objects.all()
    serializer_class = StoriLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        instance.delete()
    
class StoriViewViewSet(viewsets.ModelViewSet):
    queryset = StoriView.objects.all()
    serializer_class = StoriViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return StoriView.objects.filter(user=user)
    def perform_destroy(self, instance):
        instance.delete()   

class StoriCommentViewSet(viewsets.ModelViewSet):
    queryset = StoriComment.objects.all()
    serializer_class = StoriCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return StoriComment.objects.filter(author=user)
    def perform_destroy(self, instance):
        instance.delete()

class StoriMediaViewSet(viewsets.ModelViewSet):
    queryset = StoriMedia.objects.all()
    serializer_class = StoriMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return StoriMedia.objects.filter(author=user)
    def perform_destroy(self, instance):
        instance.delete()

