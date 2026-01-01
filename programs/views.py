from rest_framework import generics, views, status, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import EducationalProgram, Discipline
from .serializers import EducationalProgramSerializer, EducationalProgramListSerializer
from .analysis import CompetencyAnalyzer
from .filters import ProgramFilter
from .services import ExcelParser, ProgramImporter, InvalidProgramError
from users.permissions import IsStaffOrAdminOrReadOnly


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProgramListView(generics.ListCreateAPIView):
    queryset = EducationalProgram.objects.exclude(profile="nan")
    serializer_class = EducationalProgramListSerializer
    permission_classes = [IsStaffOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProgramFilter
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


class UploadProgramView(views.APIView):
    """
    API endpoint for uploading educational programs from Excel files.
    Only accessible by staff and admin users.
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsStaffOrAdminOrReadOnly]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate file extension
        if not file.name.endswith(".xlsx"):
            return Response(
                {"error": "Invalid file format. Only .xlsx files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get optional year parameter
        year = request.data.get("year")
        if year:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {"error": "Year must be a valid integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            parser = ExcelParser()
            importer = ProgramImporter(parser)
            program, created, error = importer.import_from_uploaded_file(file, year)

            if error:
                return Response(
                    {"error": error},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Clear cache after successful upload
            cache.clear()

            action = "created" if created else "updated"
            return Response(
                {
                    "message": f"Program successfully {action}",
                    "program": {
                        "id": program.id,
                        "aup_number": program.aup_number,
                        "profile": program.profile,
                        "year": program.year,
                    }
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except InvalidProgramError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to process file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
