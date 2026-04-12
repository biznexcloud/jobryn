from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeekersRecommendedList, RecruiterRecommendedList

router = DefaultRouter()
router.register('seekers', SeekersRecommendedList, basename='seekers-recommended')
router.register('recruiters', RecruiterRecommendedList, basename='recruiter-recommended')

urlpatterns = [
    path('', include(router.urls)),
]