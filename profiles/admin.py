from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = (
        'user', 'headline', 'job_title', 'city', 'country',
        'visibility_settings', 'availability', 'profile_strength_display'
    )
    list_filter = ('visibility_settings', 'available_for_freelance', 'availability', 'country')
    search_fields = ('user__email', 'user__name', 'headline', 'job_title', 'company')
    readonly_fields = ('profile_strength_display',)
    date_hierarchy = None

    fieldsets = (
        ('👤 Basic', {
            'fields': ('user', 'profile_picture', 'cover_photo', 'headline', 'about', 'pronouns')
        }),
        ('📍 Location', {
            'fields': ('city', 'state', 'country')
        }),
        ('💼 Professional', {
            'fields': ('job_title', 'company', 'experience_years', 'skills', 'education', 'resume')
        }),
        ('🔗 Links', {
            'fields': ('linkedin_url', 'github_url', 'portfolio_url', 'social_links')
        }),
        ('🎯 Extras', {
            'fields': ('languages', 'interests', 'featured_items', 'professional_motto')
        }),
        ('⚙️ Settings', {
            'fields': ('visibility_settings', 'available_for_freelance', 'availability')
        }),
    )

    @display(description="Profile Strength")
    def profile_strength_display(self, obj):
        return f"{obj.profile_strength}%"
