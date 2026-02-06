import django_filters
from .models import EducationalProgram


class ProgramFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="year")
    year__gte = django_filters.NumberFilter(field_name="year", lookup_expr='gte')
    year__lte = django_filters.NumberFilter(field_name="year", lookup_expr='lte')
    education_level = django_filters.CharFilter(field_name="education_level", lookup_expr='iexact')
    faculty = django_filters.CharFilter(field_name="faculty", lookup_expr='iexact')

    class Meta:
        model = EducationalProgram
        fields = ['year', 'education_level', 'faculty']
