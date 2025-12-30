from django.urls import path
from .views import ProgramListView, ProgramDetailView

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:id>/', ProgramDetailView.as_view(), name='program-detail'),
]
