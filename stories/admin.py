from django.contrib import admin
from .models import Stori, StoriLike, StoriView, StoriComment, StoriMedia
# Register your models here.

@admin.register(Stori)
class StoriAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'visibility', 'is_active', 'views_count', 'likes_count')
    list_filter = ('visibility', 'is_active')
    search_fields = ('author__email', 'caption')

@admin.register(StoriLike)
class StoriLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'user', 'created_at')
    search_fields = ('user__email',)

@admin.register(StoriView)
class StoriViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'user', 'viewed_at')
    search_fields = ('user__email',)

@admin.register(StoriComment)
class StoriCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'author', 'content', 'created_at')
    search_fields = ('author__email', 'content')

@admin.register(StoriMedia)
class StoriMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'author', 'created_at')
    search_fields = ('author__email',)
    
