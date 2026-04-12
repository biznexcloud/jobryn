import django_filters
from .models import Education

class EducationFilter(django_filters.FilterSet):
    school = django_filters.CharFilter(lookup_expr='icontains')
    field = django_filters.CharFilter(field_name='field_of_study', lookup_expr='icontains')

    class Meta:
        model = Education
        fields = ['school', 'field']
