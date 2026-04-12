from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Course, Enrollment


class EnrollmentInline(TabularInline):
    model = Enrollment
    fields = ('user', 'progress', 'completed', 'enrolled_at')
    readonly_fields = ('enrolled_at',)
    extra = 0
    show_change_link = True


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = (
        'title', 'instructor', 'level_badge', 'language', 'price',
        'duration_hours', 'certificate_offered', 'is_published', 'created_at'
    )
    list_filter = ('level', 'is_published', 'certificate_offered', 'language')
    search_fields = ('title', 'instructor__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [EnrollmentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('📚 Course', {
            'fields': ('title', 'instructor', 'description', 'thumbnail', 'level', 'language')
        }),
        ('📋 Content', {
            'fields': ('syllabus', 'what_you_learn', 'requirements', 'total_lectures', 'duration_hours')
        }),
        ('💰 Pricing & Status', {
            'fields': ('price', 'certificate_offered', 'is_published')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @display(description="Level", label={
        'beginner': 'success',
        'intermediate': 'warning',
        'advanced': 'danger',
    })
    def level_badge(self, obj):
        return obj.level


@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ('user', 'course', 'progress', 'completed', 'certificate_issued', 'enrolled_at')
    list_filter = ('completed', 'certificate_issued')
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('enrolled_at',)
