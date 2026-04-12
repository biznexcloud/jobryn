from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, UserSkillViewSet, EndorsementViewSet

router = DefaultRouter()
router.register(r'global', SkillViewSet, basename='skill')
router.register(r'user-skills', UserSkillViewSet, basename='user-skill')
router.register(r'endorsements', EndorsementViewSet, basename='endorsement')

urlpatterns = [
    path('', include(router.urls)),
]
