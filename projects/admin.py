from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Project


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('name', 'user', 'role', 'start_date', 'end_date')
    search_fields = ('user__email', 'name', 'role')
    date_hierarchy = 'start_date'
