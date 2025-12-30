from rest_framework import generics
from .models import EducationalProgram
from .serializers import EducationalProgramSerializer

class ProgramListView(generics.ListAPIView):
    queryset = EducationalProgram.objects.all()
    serializer_class = EducationalProgramSerializer

class ProgramDetailView(generics.RetrieveAPIView):
    queryset = EducationalProgram.objects.all()
    serializer_class = EducationalProgramSerializer
    lookup_field = 'id'
