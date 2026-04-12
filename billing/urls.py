from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Recruiter_InvoiceViewSet, Recruiter_PaymentViewSet

router = DefaultRouter()
router.register(r'invoices', Recruiter_InvoiceViewSet, basename='invoice-recruiter')
router.register(r'payments', Recruiter_PaymentViewSet, basename='payment-recruiter')

urlpatterns = [
    path('recruiter/', include(router.urls)),
]
