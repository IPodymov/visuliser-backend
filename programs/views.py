from rest_framework import generics, views, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import EducationalProgram, Discipline
from .serializers import EducationalProgramSerializer
from .analysis import CompetencyAnalyzer
from users.permissions import IsStaffOrAdminOrReadOnly


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProgramListView(generics.ListCreateAPIView):
    queryset = EducationalProgram.objects.exclude(profile="nan")
    serializer_class = EducationalProgramSerializer
    permission_classes = [IsStaffOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["education_level", "year", "faculty"]
    search_fields = ["profile", "direction", "aup_number"]


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationalProgram.objects.exclude(profile="nan")
    serializer_class = EducationalProgramSerializer
    lookup_field = "id"
    permission_classes = [IsStaffOrAdminOrReadOnly]


class ProgramAnalysisView(views.APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, id):
        program = get_object_or_404(
            EducationalProgram.objects.exclude(profile="nan"), id=id
        )
        disciplines = program.disciplines.all()

        analyzer = CompetencyAnalyzer()
        result = analyzer.analyze(disciplines)

        return Response(
            {
                "program": f"{program.aup_number} - {program.profile}",
                "analysis": result,
                "legend": CompetencyAnalyzer.DESCRIPTIONS,
            }
        )


class CompareProgramsView(views.APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        ids = request.query_params.getlist("ids")
        if not ids:
            return Response(
                {"error": "No program IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        programs = EducationalProgram.objects.filter(id__in=ids).exclude(profile="nan")
        analyzer = CompetencyAnalyzer()

        results = []
        for program in programs:
            analysis = analyzer.analyze(program.disciplines.all())
            results.append(
                {
                    "id": program.id,
                    "name": f"{program.aup_number} - {program.profile}",
                    "analysis": analysis,
                }
            )

        return Response({"results": results, "legend": CompetencyAnalyzer.DESCRIPTIONS})
