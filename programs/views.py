from rest_framework import generics, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import EducationalProgram, Discipline
from .serializers import EducationalProgramSerializer
from .analysis import CompetencyAnalyzer

class ProgramListView(generics.ListAPIView):
    queryset = EducationalProgram.objects.all()
    serializer_class = EducationalProgramSerializer

class ProgramDetailView(generics.RetrieveAPIView):
    queryset = EducationalProgram.objects.all()
    serializer_class = EducationalProgramSerializer
    lookup_field = 'id'

class ProgramAnalysisView(views.APIView):
    def get(self, request, id):
        program = get_object_or_404(EducationalProgram, id=id)
        disciplines = program.disciplines.all()
        
        analyzer = CompetencyAnalyzer()
        result = analyzer.analyze(disciplines)
        
        return Response({
            "program": f"{program.aup_number} - {program.profile}",
            "analysis": result
        })

class CompareProgramsView(views.APIView):
    def get(self, request):
        ids = request.query_params.getlist('ids')
        if not ids:
            return Response({"error": "No program IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        programs = EducationalProgram.objects.filter(id__in=ids)
        analyzer = CompetencyAnalyzer()
        
        results = []
        for program in programs:
            analysis = analyzer.analyze(program.disciplines.all())
            results.append({
                "id": program.id,
                "name": f"{program.aup_number} - {program.profile}",
                "analysis": analysis
            })
            
        return Response(results)
