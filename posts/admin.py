from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Post, Comment, Like


class CommentInline(TabularInline):
    model = Comment
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0
    show_change_link = True


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = (
        'author', 'content_preview', 'visibility_badge',
        'likes_count', 'comments_count', 'is_edited', 'created_at'
    )
    list_filter = ('visibility', 'is_edited')
    search_fields = ('author__email', 'content')
    readonly_fields = ('likes_count', 'comments_count', 'created_at', 'updated_at')
    inlines = [CommentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('📝 Content', {
            'fields': ('author', 'content', 'image', 'video', 'shared_post')
        }),
        ('⚙️ Settings', {
            'fields': ('visibility', 'is_edited')
        }),
        ('📊 Metrics', {
            'fields': ('likes_count', 'comments_count')
        }),
    )

    @display(description="Content")
    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content

    @display(description="Visibility", label={
        'public': 'success',
        'connections': 'info',
        'private': '',
    })
    def visibility_badge(self, obj):
        return obj.visibility


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at')
    search_fields = ('author__email', 'content')
    readonly_fields = ('created_at',)

    @display(description="Comment")
    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)
