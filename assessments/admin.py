from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Assessment, Question, Choice, AssessmentAttempt, UserAssessmentBadge
# Register your models here.

@admin.register(Assessment)
class AssessmentAdmin(ModelAdmin):
    list_display = ('title', 'difficulty', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description')
    
@admin.register(Question)  
class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'assessment', 'created_at')
    search_fields = ('text',)

@admin.register(Choice)
class ChoiceAdmin(ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)
    
@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(ModelAdmin):
    list_display = ('user', 'assessment', 'status', 'score', 'is_passed', 'started_at', 'completed_at')
    list_filter = ('status', 'is_passed')
    search_fields = ('user__email', 'assessment__title')
    
@admin.register(UserAssessmentBadge)
class UserAssessmentBadgeAdmin(ModelAdmin):
    list_display = ('user', 'assessment', 'issued_at')
    search_fields = ('user__email', 'assessment__title', 'badge_name')
    


