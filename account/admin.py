from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'email', 'name', 'role_badge', 'phone',
        'is_email_verified', 'is_verified_recruiter', 'is_active', 'created_at'
    )
    list_filter = ('role', 'is_email_verified', 'is_verified_recruiter', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('🔐 Authentication', {
            'fields': ('email', 'password', 'name', 'role')
        }),
        ('📱 Contact', {
            'fields': ('phone', 'alternate_phone')
        }),
        ('✅ Verification', {
            'fields': ('is_email_verified', 'is_identity_verified', 'is_verified_recruiter', 'two_factor_enabled')
        }),
        ('🌍 Locale & Security', {
            'fields': ('preferred_language', 'timezone', 'last_login_ip')
        }),
        ('⚙️ System', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login'),
        }),
    )

    @display(description="Role", label={
        'job_seeker': 'info',
        'recruiter': 'success',
        'admin': 'warning',
    })
    def role_badge(self, obj):
        return obj.role
