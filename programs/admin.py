from django.contrib import admin
from .models import (
    EducationalProgram,
    ProgramDiscipline,
    Discipline,
    Faculty,
    Direction,
    EducationLevel,
    EducationType,
    Qualification,
    StandardType,
    Semester,
    DisciplineBlock,
    DisciplinePart,
    DisciplineModule,
    LoadType,
    DisciplineMarking,
    SemesterControl
)

@admin.register(EducationalProgram)
class EducationalProgramAdmin(admin.ModelAdmin):
    list_display = ('profile', 'direction', 'year', 'faculty')
    list_filter = ('year', 'faculty', 'education_level')
    search_fields = ('profile', 'direction__name')

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProgramDiscipline)
class ProgramDisciplineAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'code', 'program', 'semester', 'load_type')
    list_filter = ('semester', 'load_type', 'program__faculty')
    search_fields = ('discipline__name', 'code')

    def get_name(self, obj):
        return obj.discipline.name
    get_name.short_description = 'Дисциплина'

# Register other models
admin.site.register(Faculty)
admin.site.register(Direction)
admin.site.register(EducationLevel)
admin.site.register(EducationType)
admin.site.register(Qualification)
admin.site.register(StandardType)
admin.site.register(Semester)
admin.site.register(DisciplineBlock)
admin.site.register(DisciplinePart)
admin.site.register(DisciplineModule)
admin.site.register(LoadType)
admin.site.register(DisciplineMarking)
admin.site.register(SemesterControl)
