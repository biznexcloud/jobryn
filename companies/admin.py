from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from jobs.admin import JobInlineForCompany
from .models import Company


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'owner', 'industry', 'company_size', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'company_size', 'industry')
    search_fields = ('name', 'owner__email', 'industry', 'location')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [JobInlineForCompany]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('🏢 Company', {
            'fields': ('owner', 'name', 'logo', 'cover_image', 'tagline', 'description')
        }),
        ('📋 Business Details', {
            'fields': ('industry', 'company_size', 'founded_year', 'headquarters', 'location')
        }),
        ('📝 Registration', {
            'fields': ('registration_number', 'tax_number', 'is_verified')
        }),
        ('🔗 Contact & Links', {
            'fields': ('website', 'email', 'phone', 'social_links')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
