from django.core.management.base import BaseCommand
from programs.models import (
    EducationalProgram,
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

class Command(BaseCommand):
    help = 'Wipes all data from the database to start fresh.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting all data...'))
        
        # Delete dependent models first
        DisciplineMarking.objects.all().delete()
        SemesterControl.objects.all().delete()
        Discipline.objects.all().delete()
        EducationalProgram.objects.all().delete()
        
        # Delete dictionaries
        Faculty.objects.all().delete()
        Direction.objects.all().delete()
        EducationLevel.objects.all().delete()
        EducationType.objects.all().delete()
        Qualification.objects.all().delete()
        StandardType.objects.all().delete()
        Semester.objects.all().delete()
        DisciplineBlock.objects.all().delete()
        DisciplinePart.objects.all().delete()
        DisciplineModule.objects.all().delete()
        LoadType.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all data.'))
