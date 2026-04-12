from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSeeker_ApplicationViewSet, Recruiter_ApplicationViewSet

seeker_router = DefaultRouter()
seeker_router.register(r'', JobSeeker_ApplicationViewSet, basename='application-seeker')

recruiter_router = DefaultRouter()
recruiter_router.register(r'', Recruiter_ApplicationViewSet, basename='application-recruiter')

urlpatterns = [
    path('seeker/', include(seeker_router.urls)),
    path('recruiter/', include(recruiter_router.urls)),
]
