from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Newsletter, Subscriber


class SubscriberInline(TabularInline):
    model = Subscriber
    fields = ('email', 'user', 'is_active', 'subscribed_at')
    readonly_fields = ('subscribed_at',)
    extra = 0


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ('title', 'frequency', 'status_badge', 'sent_at', 'created_at')
    list_filter = ('frequency', 'status')
    search_fields = ('title', 'subject', 'content')
    readonly_fields = ('created_at', 'sent_at')
    date_hierarchy = 'created_at'

    @display(description="Status", label={
        'draft': '',
        'sent': 'success',
        'scheduled': 'info',
    })
    def status_badge(self, obj):
        return obj.status


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ('email', 'user', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email', 'user__email')
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
