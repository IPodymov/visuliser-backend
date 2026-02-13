from rest_framework import viewsets, filters, status, views
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .models import EducationalProgram, ProgramDiscipline, Semester
from .serializers import (
    EducationalProgramListSerializer,
    EducationalProgramSerializer,
    ProgramDisciplineSerializer,
)
from .filters import ProgramFilter, DisciplineFilter
from .services import ExcelParser, ProgramImporter
from rest_framework.response import Response
from rest_framework.decorators import action


class EducationalProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing educational programs.
    """

    queryset = EducationalProgram.objects.select_related(
        "education_type",
        "education_level",
        "direction",
        "qualification",
        "standard_type",
        "faculty",
    ).prefetch_related(
        Prefetch(
            "disciplines",
            queryset=ProgramDiscipline.objects.select_related(
                "discipline", "semester", "block", "part", "module", "load_type"
            ).order_by("semester__name", "discipline__name"),
        )
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProgramFilter
    search_fields = ["profile", "direction__name", "direction__code", "faculty__name"]
    ordering_fields = ["year", "direction__name", "profile"]

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return EducationalProgramListSerializer
        return EducationalProgramSerializer

    @action(detail=True, methods=["get"])
    def disciplines(self, request, pk=None):
        """
        Get disciplines for a specific program, optionally filtered by semester.
        """
        program = self.get_object()
        disciplines = ProgramDiscipline.objects.filter(program=program).select_related(
            "semester", "block", "part", "module", "load_type", "discipline"
        )

        # Apply semester filter if provided via query params
        semester = request.query_params.get("semester")
        if semester:
            disciplines = disciplines.filter(semester__name__icontains=semester)

        serializer = ProgramDisciplineSerializer(disciplines, many=True)
        return Response(serializer.data)


class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing disciplines.
    """

    queryset = ProgramDiscipline.objects.select_related(
        "discipline",
        "program",
        "program__direction",
        "program__faculty",
        "semester",
        "block",
        "part",
        "module",
        "load_type",
    ).all()
    serializer_class = ProgramDisciplineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DisciplineFilter
    search_fields = ["discipline__name", "code", "program__profile", "semester__name"]
    ordering_fields = ["discipline__name", "code", "semester__name"]


class UploadProgramView(views.APIView):
    """
    View for uploading a program Excel file.
    """

    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        year = request.data.get("year")

        parser = ExcelParser()
        importer = ProgramImporter(parser)

        try:
            program, created, error = importer.import_from_uploaded_file(file_obj, year=year)
            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EducationalProgramSerializer(program)
            response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=response_status)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
