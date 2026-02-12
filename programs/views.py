from rest_framework import viewsets, filters, status, views
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import EducationalProgram, Discipline, Semester
from .serializers import (
    EducationalProgramListSerializer,
    EducationalProgramSerializer,
    DisciplineSerializer,
)
from .filters import ProgramFilter, DisciplineFilter
from .services import ExcelParser, ProgramImporter
from rest_framework.response import Response
from rest_framework.decorators import action


class EducationalProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing educational programs.
    """

    queryset = EducationalProgram.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProgramFilter
    search_fields = ["profile", "direction__name", "direction__code", "faculty__name"]
    ordering_fields = ["year", "direction__name", "profile"]

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
        disciplines = Discipline.objects.filter(program=program)

        # Apply semester filter if provided via query params
        semester = request.query_params.get("semester")
        if semester:
            disciplines = disciplines.filter(semester__name__icontains=semester)

        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data)


class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing disciplines.
    """

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DisciplineFilter
    search_fields = ["name", "code", "program__profile", "semester__name"]
    ordering_fields = ["name", "code", "semester__name"]


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
