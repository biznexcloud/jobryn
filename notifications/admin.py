from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('recipient', 'sender', 'type_badge', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('recipient__email', 'sender__email', 'message', 'title')
    readonly_fields = ('created_at', 'read_at')
    date_hierarchy = 'created_at'

    @display(description="Type", label={
        'connection_request': 'info',
        'connection_accepted': 'success',
        'message': 'warning',
        'application_update': 'warning',
        'post_like': '',
        'post_comment': '',
        'meeting_scheduled': 'info',
        'system': 'danger',
    })
    def type_badge(self, obj):
        return obj.notification_type
