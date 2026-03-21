from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(ModelAdmin):
    list_display = (
        'application_detail', 'interviewer', 'meeting_type_badge',
        'scheduled_at', 'duration_minutes', 'status_badge'
    )
    list_filter = ('meeting_type', 'status', 'candidate_no_show')
    search_fields = ('application__seeker__email', 'application__job__title', 'interviewer__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'scheduled_at'

    fieldsets = (
        ('📅 Meeting', {
            'fields': ('application', 'interviewer', 'meeting_type', 'scheduled_at', 'duration_minutes')
        }),
        ('🔗 Location', {
            'fields': ('meeting_link', 'location_address', 'recording_url')
        }),
        ('📋 Notes', {
            'fields': ('agenda', 'notes', 'feedback')
        }),
        ('⚙️ Status', {
            'fields': ('status', 'candidate_no_show')
        }),
    )

    @display(description="Seeker → Job")
    def application_detail(self, obj):
        return f"{obj.application.seeker.email} → {obj.application.job.title}"

    @display(description="Type", label={
        'online': 'info',
        'onsite': 'success',
        'phone': 'warning',
    })
    def meeting_type_badge(self, obj):
        return obj.meeting_type

    @display(description="Status", label={
        'scheduled': 'info',
        'completed': 'success',
        'cancelled': 'danger',
        'rescheduled': 'warning',
        'no_show': '',
    })
    def status_badge(self, obj):
        return obj.status
