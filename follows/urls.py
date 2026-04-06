from django.urls import path
from .views import (
    FollowUserView,
    UnfollowUserView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('follow/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:pk>/', FollowersListView.as_view(), name='followers-list'),
    path('following/<int:pk>/', FollowingListView.as_view(), name='following-list'),
]