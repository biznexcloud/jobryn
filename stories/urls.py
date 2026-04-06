from stories.views import StoriViewSet, StoriLikeViewSet, StoriViewViewSet, StoriCommentViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'stori', StoriViewSet, basename='stori') 
router.register(r'stori-likes', StoriLikeViewSet, basename='stori-like')
router.register(r'stori-views', StoriViewViewSet, basename='stori-view')
router.register(r'stori-comments', StoriCommentViewSet, basename='stori-comment')
urlpatterns = router.urls

from django.urls import path, include
urlpatterns = [
    path('', include(router.urls)),
]