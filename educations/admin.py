from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Education


@admin.register(Education)
class EducationAdmin(ModelAdmin):
    list_display = ('user', 'school', 'degree', 'field_of_study', 'start_date', 'end_date')
    search_fields = ('user__email', 'school', 'degree', 'field_of_study')
    date_hierarchy = 'start_date'
