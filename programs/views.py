from rest_framework import generics, views, status, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import EducationalProgram
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
        program = get_object_or_404(EducationalProgram.objects.exclude(profile="nan"), id=id)
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
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file extension
        if not file.name.endswith(".xlsx"):
            return Response(
                {"error": "Invalid file format. Only .xlsx files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get optional year parameter
        year = request.data.get("year")
        if year:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {"error": "Year must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            parser = ExcelParser()
            importer = ProgramImporter(parser)
            program, created, error = importer.import_from_uploaded_file(file, year)

            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

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
                    },
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except InvalidProgramError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to process file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ComparisonChartDataView(views.APIView):
    """
    Возвращает данные для построения графиков сравнения программ
    """

    def get(self, request):
        ids = request.query_params.getlist("ids")
        # competency, disciplines, credits
        chart_type = request.query_params.get("type", "competency")

        if not ids:
            return Response(
                {"error": "No program IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        programs = EducationalProgram.objects.filter(id__in=ids).exclude(profile="nan")

        if chart_type == "competency":
            return self._get_competency_comparison(programs)
        elif chart_type == "disciplines":
            return self._get_disciplines_comparison(programs)
        elif chart_type == "credits":
            return self._get_credits_comparison(programs)

        return Response(
            {"error": f"Unknown chart type: {chart_type}"}, status=status.HTTP_400_BAD_REQUEST
        )

    def _get_competency_comparison(self, programs):
        analyzer = CompetencyAnalyzer()
        data = {"labels": list(CompetencyAnalyzer.DESCRIPTIONS.keys()), "datasets": []}

        for program in programs:
            analysis = analyzer.analyze(program.disciplines.all())
            data["datasets"].append(
                {
                    "label": (
                        f"{program.profile} ({program.year})" if program.year else program.profile
                    ),
                    "data": [analysis.get(label, 0) for label in data["labels"]],
                    "program_id": program.id,
                }
            )

        return Response({"type": "bar", "data": data, "legend": CompetencyAnalyzer.DESCRIPTIONS})

    def _get_credits_comparison(self, programs):
        """Сравнение по количеству ЗЕТ (зачётных единиц) по блокам"""
        import re

        data = {"labels": [], "datasets": []}

        # First pass to collect all unique blocks to ensure consistent labels
        all_blocks = set()
        for program in programs:
            for discipline in program.disciplines.all():
                block = discipline.block or "Без блока"
                all_blocks.add(block)

        # Sort blocks for consistency
        data["labels"] = sorted(list(all_blocks))

        for program in programs:
            blocks_data = {block: 0 for block in data["labels"]}
            for discipline in program.disciplines.all():
                block = discipline.block or "Без блока"
                try:
                    # Clean zet string (replace comma with dot if needed)
                    zet_str = str(discipline.zet).replace(",", ".") if discipline.zet else "0"
                    # Handle ranges or non-numeric by taking first number or 0
                    match = re.search(r"[-+]?\d*\.\d+|\d+", zet_str)
                    zet = float(match.group()) if match else 0
                except (ValueError, TypeError):
                    zet = 0
                blocks_data[block] += zet

            data["datasets"].append(
                {"label": program.profile, "data": [blocks_data[label] for label in data["labels"]]}
            )

        return Response({"type": "bar", "data": data})

    def _get_disciplines_comparison(self, programs):
        """Сравнение количества дисциплин по семестрам или всего"""
        # Basic implementation: Total count of disciplines
        data = {
            "labels": [f"{p.profile} ({p.year})" if p.year else p.profile for p in programs],
            "datasets": [
                {"label": "Количество дисциплин", "data": [p.disciplines.count() for p in programs]}
            ],
        }
        return Response({"type": "bar", "data": data})
