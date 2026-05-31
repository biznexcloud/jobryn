from .views import ConnectionViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path    

router = DefaultRouter()
router.register(r'connections', ConnectionViewSet, basename='connection')

urlpatterns = [

] + router.urls