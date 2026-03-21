from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Follow


@admin.register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('follower', 'following', 'follow_type', 'created_at')
    list_filter = ('follow_type',)
    search_fields = ('follower__email', 'following__email')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
