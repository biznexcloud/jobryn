from django.urls import path
from .views import (
    SendMessageView,
    ConversationView,
    ThreadMessagesView,
    MarkAsReadView,
    DeleteMessageView,
)

urlpatterns = [
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/conversation/<int:user_id>/', ConversationView.as_view(), name='conversation'),
    path('messages/thread/<str:thread_id>/', ThreadMessagesView.as_view(), name='thread-messages'),
    path('messages/read/<int:pk>/', MarkAsReadView.as_view(), name='mark-read'),
    path('messages/delete/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'),
]