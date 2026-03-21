from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSeeker_MeetingViewSet, Recruiter_MeetingViewSet

seeker_router = DefaultRouter()
seeker_router.register(r'', JobSeeker_MeetingViewSet, basename='meeting-seeker')

recruiter_router = DefaultRouter()
recruiter_router.register(r'', Recruiter_MeetingViewSet, basename='meeting-recruiter')

urlpatterns = [
    path('seeker/', include(seeker_router.urls)),
    path('recruiter/', include(recruiter_router.urls)),
]
