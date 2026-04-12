import django_filters
from .models import Profile

class ProfileFilter(django_filters.FilterSet):
    headline = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location_override', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['headline', 'location']
