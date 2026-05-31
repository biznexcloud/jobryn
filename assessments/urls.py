# urls.py

from django.urls import path

from .views import (
    AssessmentListAPIView,
    AssessmentDetailAPIView,
    StartAssessmentAPIView,
    MyAttemptsAPIView,
    MyBadgesAPIView,
)

urlpatterns = [
    path(
        'assessments/',
        AssessmentListAPIView.as_view(),
        name='assessment-list'
    ),

    path(
        'assessments/<int:pk>/',
        AssessmentDetailAPIView.as_view(),
        name='assessment-detail'
    ),

    path(
        'assessments/<int:pk>/start/',
        StartAssessmentAPIView.as_view(),
        name='assessment-start'
    ),

    path(
        'my-attempts/',
        MyAttemptsAPIView.as_view(),
        name='my-attempts'
    ),

    path(
        'my-badges/',
        MyBadgesAPIView.as_view(),
        name='my-badges'
    ),
]