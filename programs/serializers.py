from rest_framework import serializers
from collections import defaultdict
from .models import (
    EducationalProgram,
    ProgramDiscipline,
    Semester,
    DisciplineBlock,
    DisciplinePart,
    DisciplineModule,
    LoadType,
)


class ProgramDisciplineSerializer(serializers.ModelSerializer):
    semester = serializers.StringRelatedField()
    block = serializers.StringRelatedField()
    part = serializers.StringRelatedField()
    module = serializers.StringRelatedField()
    load_type = serializers.StringRelatedField()
    name = serializers.CharField(source="discipline.name", read_only=True)

    class Meta:
        model = ProgramDiscipline
        fields = [
            "id",
            "block",
            "code",
            "part",
            "module",
            "name",
            "semester",
            "load_type",
            "amount",
            "measurement_unit",
            "zet",
        ]


class EducationalProgramListSerializer(serializers.ModelSerializer):
    education_type = serializers.StringRelatedField()
    education_level = serializers.StringRelatedField()
    direction = serializers.StringRelatedField()
    qualification = serializers.StringRelatedField()
    standard_type = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = EducationalProgram
        fields = [
            "id",
            "education_type",
            "education_level",
            "direction",
            "qualification",
            "profile",
            "standard_type",
            "faculty",
            "year",
        ]


class EducationalProgramSerializer(serializers.ModelSerializer):
    education_type = serializers.StringRelatedField()
    education_level = serializers.StringRelatedField()
    direction = serializers.StringRelatedField()
    qualification = serializers.StringRelatedField()
    standard_type = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()
    disciplines = ProgramDisciplineSerializer(many=True, read_only=True)

    class Meta:
        model = EducationalProgram
        fields = [
            "id",
            "education_type",
            "education_level",
            "direction",
            "qualification",
            "profile",
            "standard_type",
            "faculty",
            "year",
            "disciplines",
        ]

