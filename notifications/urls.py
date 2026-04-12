from django.urls import path
from notifications.views import (
    NotificationListView,
    UnreadNotificationListView,
    CreateNotificationView,
    MarkNotificationAsReadView,
    MarkAllAsReadView,
    DeleteNotificationView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notifications'),
    path('create/', CreateNotificationView.as_view(), name='create-notification'),
    path('read/<int:pk>/', MarkNotificationAsReadView.as_view(), name='mark-read'),
    path('read-all/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    path('delete/<int:pk>/', DeleteNotificationView.as_view(), name='delete-notification'),
]