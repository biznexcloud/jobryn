from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Certification


@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    list_display = ('user', 'name', 'issuing_organization', 'issue_date', 'expiration_date', 'is_expired')
    list_filter = ('is_expired', 'issuing_organization')
    search_fields = ('user__email', 'name', 'issuing_organization', 'credential_id')
    date_hierarchy = 'issue_date'
