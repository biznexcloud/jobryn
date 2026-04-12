from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Application


class MeetingInline(TabularInline):
    from meetings.models import Meeting
    model = Meeting
    fields = ('meeting_type', 'scheduled_at', 'status', 'meeting_link')
    readonly_fields = ('scheduled_at',)
    extra = 0
    show_change_link = True


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = (
        'seeker', 'job', 'status_badge', 'expected_salary',
        'accepted_salary', 'commission_paid', 'created_at'
    )
    list_filter = ('status', 'commission_paid', 'payroll_initialized')
    search_fields = ('seeker__email', 'job__title', 'job__company__name')
    readonly_fields = ('created_at', 'updated_at', 'hired_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('📋 Application', {
            'fields': ('job', 'seeker', 'status', 'resume', 'cover_letter')
        }),
        ('💰 Salary', {
            'fields': ('expected_salary', 'accepted_salary', 'payment_type')
        }),
        ('🎯 Recruiter Tools', {
            'fields': ('interview_score', 'internal_notes', 'rejection_reason', 'feedback_for_seeker')
        }),
        ('✅ Hire Status', {
            'fields': ('hired_at', 'contract_end', 'payroll_initialized', 'commission_paid')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @display(description="Status", label={
        'applied': 'info',
        'screening': 'warning',
        'online_meeting': 'warning',
        'onsite_meeting': 'warning',
        'hired': 'success',
        'rejected': 'danger',
        'withdrawn': '',
    })
    def status_badge(self, obj):
        return obj.status
