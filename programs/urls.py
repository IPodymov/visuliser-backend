from django.urls import path
from .views import ProgramListView, ProgramDetailView, ProgramAnalysisView, CompareProgramsView

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:id>/', ProgramDetailView.as_view(), name='program-detail'),
    path('programs/<int:id>/analysis/', ProgramAnalysisView.as_view(), name='program-analysis'),
    path('programs/compare/', CompareProgramsView.as_view(), name='programs-compare'),
]
