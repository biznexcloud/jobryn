from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Job


class JobInlineForCompany(TabularInline):
    model = Job
    fields = ('title', 'job_type', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0
    show_change_link = True


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = (
        'title', 'company', 'recruiter',
        'job_type_badge', 'experience_level', 'payment_type',
        'salary_min', 'salary_max', 'is_active', 'created_at'
    )
    list_filter = ('job_type', 'experience_level', 'payment_type', 'is_active', 'is_onsite', 'is_remote')
    search_fields = ('title', 'company__name', 'recruiter__email', 'location')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('📋 Job Info', {
            'fields': ('title', 'recruiter', 'company', 'description')
        }),
        ('🗺️ Details', {
            'fields': ('location', 'job_type', 'experience_level', 'payment_type', 'is_onsite', 'is_remote')
        }),
        ('💰 Compensation', {
            'fields': ('salary_min', 'salary_max', 'currency')
        }),
        ('📝 Requirements & Skills', {
            'fields': ('requirements', 'required_skills', 'benefits')
        }),
        ('⚙️ Status', {
            'fields': ('is_active', 'application_deadline', 'views_count')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @display(description="Job Type", label={
        'full_time': 'success',
        'part_time': 'warning',
        'contract': 'info',
        'internship': '',
        'freelance': 'danger',
    })
    def job_type_badge(self, obj):
        return obj.job_type
