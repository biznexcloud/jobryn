from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSeeker_ProfileViewSet, Recruiter_ProfileViewSet

seeker_router = DefaultRouter()
seeker_router.register(r'', JobSeeker_ProfileViewSet, basename='profile-seeker')

recruiter_router = DefaultRouter()
recruiter_router.register(r'', Recruiter_ProfileViewSet, basename='profile-recruiter')

urlpatterns = [
    path('seeker/', include(seeker_router.urls)),
    path('recruiter/', include(recruiter_router.urls)),
]
