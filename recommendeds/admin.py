from django.contrib import admin
from .models import Recommended
from unfold.admin import ModelAdmin
# Register your models here.
@admin.register(Recommended)
class RecommendedAdmin(ModelAdmin):
    list_display = ('user',  'job', 'created_at', )
    search_fields = ('user__email', 'recommended_user__email', 'job__title')
