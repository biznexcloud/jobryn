import django_filters
from .models import Experience

class ExperienceFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(field_name='company_name', lookup_expr='icontains')

    class Meta:
        model = Experience
        fields = ['title', 'company', 'is_current']
