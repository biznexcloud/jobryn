from rest_framework import serializers
from .models import Invoice, Payment

class Recruiter_InvoiceSerializer(serializers.ModelSerializer):
    seeker_email = serializers.ReadOnlyField(source='application.seeker.email')
    job_title = serializers.ReadOnlyField(source='application.job.title')

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class Recruiter_PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at',)
