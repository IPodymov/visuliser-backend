from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EducationalProgramViewSet, DisciplineViewSet, UploadProgramView

router = DefaultRouter()
router.register(r"programs", EducationalProgramViewSet, basename="educationalprogram")
router.register(r"disciplines", DisciplineViewSet, basename="discipline")

urlpatterns = [
    path("programs/upload/", UploadProgramView.as_view(), name="program-upload"),
    path("", include(router.urls)),
]
