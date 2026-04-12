from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Invoice, Payment, PayrollRecord


class PaymentInline(TabularInline):
    model = Payment
    fields = ('transaction_id', 'amount', 'payment_method', 'is_verified', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ('id', 'application_email', 'amount', 'tax_amount', 'total_amount', 'status_badge', 'due_date', 'created_at')
    list_filter = ('status', 'currency')
    search_fields = ('application__seeker__email', 'application__job__title')
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    inlines = [PaymentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('📄 Invoice', {
            'fields': ('application', 'status', 'currency')
        }),
        ('💰 Amounts', {
            'fields': ('amount', 'tax_amount', 'total_amount')
        }),
        ('📝 Billing', {
            'fields': ('tax_id', 'billing_address', 'invoice_notes', 'due_date', 'paid_at')
        }),
        ('💳 Khalti', {
            'fields': ('khalti_pidx',)
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @display(description="Applicant")
    def application_email(self, obj):
        return obj.application.seeker.email

    @display(description="Status", label={
        'unpaid': 'danger',
        'paid': 'success',
        'void': '',
        'overdue': 'warning',
    })
    def status_badge(self, obj):
        return obj.status


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('transaction_id', 'invoice', 'amount', 'payment_method', 'is_verified', 'created_at')
    list_filter = ('payment_method', 'is_verified')
    search_fields = ('transaction_id', 'invoice__application__seeker__email')
    readonly_fields = ('created_at',)


@admin.register(PayrollRecord)
class PayrollRecordAdmin(ModelAdmin):
    list_display = (
        'application_email', 'salary_amount', 'commission_amount',
        'gross_amount', 'total_payable', 'pay_period_end', 'status_badge'
    )
    list_filter = ('status',)
    search_fields = ('application__seeker__email',)
    readonly_fields = ('gross_amount', 'total_payable', 'created_at', 'updated_at')
    date_hierarchy = 'pay_period_end'

    @display(description="Employee")
    def application_email(self, obj):
        return obj.application.seeker.email

    @display(description="Status", label={
        'pending': 'warning',
        'processing': 'info',
        'paid': 'success',
        'cancelled': 'danger',
    })
    def status_badge(self, obj):
        return obj.status
