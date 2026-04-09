from django.urls import path
from .views import (
    SendConnectionRequestView,
    RespondConnectionRequestView,
    CancelConnectionRequestView,
    ConnectionListView,
    IncomingConnectionListView,
)

urlpatterns = [
    path('connect/', SendConnectionRequestView.as_view(), name='send-connection'),
    path('connect/respond/<int:pk>/', RespondConnectionRequestView.as_view(), name='respond-connection'),
    path('connect/cancel/<int:pk>/', CancelConnectionRequestView.as_view(), name='cancel-connection'),
    path('connections/', ConnectionListView.as_view(), name='my-connections'),
    path('connections/incoming/', IncomingConnectionListView.as_view(), name='incoming-connections'),
]