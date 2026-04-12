from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Connection


@admin.register(Connection)
class ConnectionAdmin(ModelAdmin):
    list_display = ('sender', 'receiver', 'status_badge', 'accepted_at', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender__email', 'receiver__email')
    readonly_fields = ('created_at', 'accepted_at')
    date_hierarchy = 'created_at'

    @display(description="Status", label={
        'pending': 'warning',
        'accepted': 'success',
        'declined': 'danger',
        'blocked': '',
    })
    def status_badge(self, obj):
        return obj.status
