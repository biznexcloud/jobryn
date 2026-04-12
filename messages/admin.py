from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Message


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('sender', 'receiver', 'content_preview', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('sender__email', 'receiver__email', 'thread_id')
    readonly_fields = ('created_at', 'read_at')
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = "Message"
