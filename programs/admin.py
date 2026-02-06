from django.contrib import admin
from .models import EducationalProgram, Discipline


@admin.register(EducationalProgram)
class EducationalProgramAdmin(admin.ModelAdmin):
    list_display = ("aup_number", "profile", "direction_code", "faculty", "year", "education_level")
    list_filter = ("year", "faculty", "education_level", "education_type")
    search_fields = ("aup_number", "profile", "direction", "direction_code")
    ordering = ("-year", "aup_number")


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "program", "zet", "period", "block")
    list_filter = ("block", "part", "period")
    search_fields = ("name", "code", "program__profile", "program__aup_number")
    list_select_related = ("program",)
