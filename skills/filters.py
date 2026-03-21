import django_filters
from .models import Skill

class SkillFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Skill
        fields = ['name']
