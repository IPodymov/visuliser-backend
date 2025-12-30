from rest_framework import serializers
from .models import EducationalProgram, Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'block', 'code', 'part', 'module', 'record_type', 'name', 'period', 'load_type', 'amount', 'measurement_unit', 'zet']

class EducationalProgramSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)

    class Meta:
        model = EducationalProgram
        fields = ['id', 'aup_number', 'education_type', 'education_level', 'direction', 'direction_code', 'qualification', 'profile', 'standard_type', 'faculty', 'year', 'disciplines']
