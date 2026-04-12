from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Skill, UserSkill, Endorsement


class UserSkillInline(TabularInline):
    model = UserSkill
    fields = ('user', 'proficiency_level', 'years_of_experience', 'is_featured')
    extra = 0
    show_change_link = True


class EndorsementInline(TabularInline):
    model = Endorsement
    fields = ('endorser', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    inlines = [UserSkillInline]
    ordering = ['name']


@admin.register(UserSkill)
class UserSkillAdmin(ModelAdmin):
    list_display = ('user', 'skill', 'proficiency_level', 'years_of_experience', 'is_featured', 'created_at')
    list_filter = ('proficiency_level', 'is_featured')
    search_fields = ('user__email', 'skill__name')
    readonly_fields = ('created_at',)
    inlines = [EndorsementInline]
