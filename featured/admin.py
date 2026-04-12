from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import FeaturedItem

@admin.register(FeaturedItem)
class FeaturedItemAdmin(ModelAdmin):
    list_display = ('user', 'priority', 'content_type', 'object_id', 'created_at')
    list_filter = ('priority', 'created_at')
