import django_filters
from .models import EducationalProgram, Discipline


class ProgramFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="year")
    year__gte = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year__lte = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    education_level = django_filters.CharFilter(
        field_name="education_level__name", lookup_expr="icontains"
    )
    faculty = django_filters.CharFilter(field_name="faculty__name", lookup_expr="icontains")
    direction = django_filters.CharFilter(field_name="direction__name", lookup_expr="icontains")
    profile = django_filters.CharFilter(field_name="profile", lookup_expr="icontains")

    class Meta:
        model = EducationalProgram
        fields = ["year", "education_level", "faculty", "direction", "profile"]


class DisciplineFilter(django_filters.FilterSet):
    semester = django_filters.CharFilter(field_name="semester__name", lookup_expr="icontains")
    program = django_filters.NumberFilter(field_name="program__id")

    class Meta:
        model = Discipline
        fields = ["semester", "program"]
