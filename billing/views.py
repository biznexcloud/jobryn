from rest_framework import viewsets, permissions
from .models import Invoice, Payment

from .serializers import Recruiter_InvoiceSerializer, Recruiter_PaymentSerializer
from jobrynbackend.permissions import IsRecruiter

class Recruiter_InvoiceViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to manage invoices for their job applications.
    """
    serializer_class = Recruiter_InvoiceSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Invoice.objects.none()
        return Invoice.objects.filter(application__job__recruiter=self.request.user)

class Recruiter_PaymentViewSet(viewsets.ModelViewSet):
    """
    API for Recruiters to track their payments.
    """
    serializer_class = Recruiter_PaymentSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Payment.objects.none()
        return Payment.objects.filter(invoice__application__job__recruiter=self.request.user)
