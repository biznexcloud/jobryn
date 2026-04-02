from django.db import models
from applications.models import Application


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('overdue', 'Overdue'),
    )

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='invoice')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='NPR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True)
    notes = models.TextField(blank=True)

    # 📝 BILLING DETAILS
    tax_id = models.CharField(max_length=50, blank=True)
    billing_address = models.TextField(blank=True)
    invoice_notes = models.TextField(blank=True)
    invoice_no = models.CharField(max_length=100, unique=True, blank=True)  # Auto-generated invoice number

    # 💳 KHALTI SPECIFIC
    khalti_pidx = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.pk} — {self.application.seeker.email} [{self.status}]"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default='khalti'
    )
    payment_details = models.JSONField(default=dict, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['invoice', 'is_verified']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id} [{self.payment_method}]"


class PayrollRecord(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payroll_records')
    salary_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # salary + commission
    total_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # gross + tax
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payroll Record'
        verbose_name_plural = 'Payroll Records'
        indexes = [
            models.Index(fields=['application', 'status']),
            models.Index(fields=['pay_period_end']),
        ]

    def save(self, *args, **kwargs):
        self.gross_amount = self.salary_amount + self.commission_amount
        self.total_payable = self.gross_amount + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll — {self.application.seeker.email} | {self.pay_period_start} to {self.pay_period_end} [{self.status}]"
