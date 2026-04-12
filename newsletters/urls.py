from django.urls import path
from .views import (
    SubscribeView,
    UnsubscribeView,
    NewsletterCreateView,
    NewsletterListView,
    SendNewsletterView,
)

urlpatterns = [
    path('subscribe/', SubscribeView.as_view()),
    path('unsubscribe/', UnsubscribeView.as_view()),
    path('newsletters/', NewsletterListView.as_view()),
    path('newsletters/create/', NewsletterCreateView.as_view()),
    path('newsletters/send/', SendNewsletterView.as_view()),
]