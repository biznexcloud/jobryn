from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Experience


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ('user', 'title', 'company_name', 'employment_type', 'start_date', 'end_date', 'is_current')
    list_filter = ('employment_type', 'location_type', 'is_current')
    search_fields = ('user__email', 'title', 'company_name')
    date_hierarchy = 'start_date'
