from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSeeker_JobViewSet, Recruiter_JobViewSet

seeker_router = DefaultRouter()
seeker_router.register(r'', JobSeeker_JobViewSet, basename='job-seeker')

recruiter_router = DefaultRouter()
recruiter_router.register(r'', Recruiter_JobViewSet, basename='job-recruiter')

urlpatterns = [
    path('seeker/', include(seeker_router.urls)),
    path('recruiter/', include(recruiter_router.urls)),
]
