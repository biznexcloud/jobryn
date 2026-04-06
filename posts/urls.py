from .views import PostViewSet, CommentViewSet, LikeViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
# router.register(r'post-visibility', PostVisibilityViewSet)
# router.register(r'post-shares', PostShareViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')


urlpatterns = [
    path('', include(router.urls)),
]
